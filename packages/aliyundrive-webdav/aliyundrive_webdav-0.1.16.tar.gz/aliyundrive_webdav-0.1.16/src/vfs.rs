use std::io::SeekFrom;
use std::path::Path;
use std::time::Duration;

use anyhow::Result;
use bytes::{Buf, Bytes};
use futures_util::future::{self, FutureExt};
use moka::future::{Cache, CacheBuilder};
use tokio::{sync::oneshot, time::timeout};
use tracing::{debug, error, trace};
use webdav_handler::{
    davpath::DavPath,
    fs::{
        DavDirEntry, DavFile, DavFileSystem, DavMetaData, FsError, FsFuture, FsStream, OpenOptions,
        ReadDirMeta,
    },
};

use crate::drive::{AliyunDrive, AliyunFile};

#[derive(Copy, Clone, Debug)]
#[allow(non_camel_case_types)]
struct ENCODE_SET;

impl percent_encoding::EncodeSet for ENCODE_SET {
    // Encode all non-unreserved characters, except '/'.
    // See RFC3986, and https://en.wikipedia.org/wiki/Percent-encoding .
    #[inline]
    fn contains(&self, byte: u8) -> bool {
        let unreserved = (b'A'..=b'Z').contains(&byte)
            || (b'a'..=b'z').contains(&byte)
            || (b'0'..=b'9').contains(&byte)
            || byte == b'-'
            || byte == b'_'
            || byte == b'.'
            || byte == b'~';
        !unreserved && byte != b'/'
    }
}

// encode path segment with user-defined ENCODE_SET
fn encode_path(src: &[u8]) -> String {
    percent_encoding::percent_encode(src, ENCODE_SET).to_string()
}

#[derive(Clone)]
pub struct AliyunDriveFileSystem {
    drive: AliyunDrive,
    dir_cache: Cache<String, Vec<AliyunFile>>,
}

impl AliyunDriveFileSystem {
    pub async fn new(refresh_token: String, cache_size: usize) -> Result<Self> {
        let drive = AliyunDrive::new(refresh_token).await?;
        let dir_cache = CacheBuilder::new(cache_size)
            .time_to_live(Duration::from_secs(60 * 60))
            .time_to_idle(Duration::from_secs(30 * 60))
            .build();
        debug!("dir cache initialized");
        Ok(Self { drive, dir_cache })
    }

    fn find_in_cache(&self, path: &Path) -> Result<Option<AliyunFile>, FsError> {
        if let Some(parent) = path.parent() {
            let parent_str = parent.to_string_lossy().into_owned();
            let file_name = path
                .file_name()
                .ok_or(FsError::NotFound)?
                .to_string_lossy()
                .into_owned();
            let file = self.dir_cache.get(&parent_str).and_then(|files| {
                for file in &files {
                    if file.name == file_name {
                        return Some(file.clone());
                    }
                }
                None
            });
            Ok(file)
        } else {
            let root = AliyunFile::new_root();
            Ok(Some(root))
        }
    }

    async fn get_file(&self, dav_path: &DavPath) -> Result<Option<AliyunFile>, FsError> {
        let path = dav_path.as_rel_ospath();
        let path_str = path.to_string_lossy().into_owned();
        let file = self.find_in_cache(path)?;
        if let Some(file) = file {
            trace!("found {} file: {} in cache", path_str, file.id);
            Ok(Some(file))
        } else {
            trace!("{} file not found in cache", path_str);
            let parts: Vec<&str> = path_str.split('/').collect();
            let parts_len = parts.len();
            let filename = parts[parts_len - 1];

            // find in root first
            let mut files = self.read_dir_and_cache(&DavPath::new("/").unwrap()).await?;
            if let Some(file) = files.iter().find(|f| f.name == filename) {
                trace!("found {} file: {}", path_str, file.id);
                return Ok(Some(file.clone()));
            }

            let mut prefix = String::new();
            for part in &parts[0..parts_len - 1] {
                let parent = format!("{}/{}", prefix, part);
                let parent_path = DavPath::new(&encode_path(parent.as_bytes()))
                    .map_err(|_| FsError::GeneralFailure)?;
                prefix = parent;
                files = self.read_dir_and_cache(&parent_path).await?;
                if let Some(file) = files.iter().find(|f| f.name == filename) {
                    trace!("found {} file: {}", path_str, file.id);
                    return Ok(Some(file.clone()));
                }
            }
            Ok(None)
        }
    }

    async fn read_dir_and_cache(&self, path: &DavPath) -> Result<Vec<AliyunFile>, FsError> {
        let path = path.as_rel_ospath();
        debug!(path = %path.display(), "read_dir and cache");
        let path_str = path.to_string_lossy().into_owned();
        let parent_file_id = if path_str.is_empty() {
            "root".to_string()
        } else {
            self.find_in_cache(path)?.ok_or(FsError::NotFound)?.id
        };
        let files = if let Some(files) = self.dir_cache.get(&path_str) {
            let this = self.clone();
            let (tx, rx) = oneshot::channel();
            tokio::spawn(async move {
                match this
                    .list_files_and_cache(path_str.clone(), parent_file_id)
                    .await
                {
                    Ok(items) => {
                        trace!(path = %path_str, "refresh directory file list succeed");
                        if let Err(_) = tx.send(items) {
                            trace!("read_dir_and_cache: the receiver dropped");
                        }
                    }
                    Err(err) => error!(error = ?err, "refresh directory file list failed"),
                }
            });
            match timeout(Duration::from_secs(1), rx).await {
                Ok(items) => items.unwrap_or(files),
                Err(_) => files,
            }
        } else {
            self.list_files_and_cache(path_str, parent_file_id)
                .await
                .map_err(|_| FsError::NotFound)?
        };
        Ok(files)
    }

    async fn list_files_and_cache(
        &self,
        path_str: String,
        parent_file_id: String,
    ) -> Result<Vec<AliyunFile>> {
        let files = self.drive.list_all(&parent_file_id).await?;
        self.cache_dir(path_str, files.clone()).await;
        Ok(files)
    }

    async fn cache_dir(&self, dir_path: String, files: Vec<AliyunFile>) {
        trace!(path = %dir_path, count = files.len(), "cache dir");
        self.dir_cache.insert(dir_path, files).await;
    }
}

impl DavFileSystem for AliyunDriveFileSystem {
    fn open<'a>(&'a self, path: &'a DavPath, _options: OpenOptions) -> FsFuture<Box<dyn DavFile>> {
        debug!(path = %path.as_rel_ospath().display(), "fs: open");
        async move {
            let file = self.get_file(path).await?.ok_or(FsError::NotFound)?;
            let download_url = self.drive.get_download_url(&file.id).await.ok();
            let dav_file = AliyunDavFile::new(self.drive.clone(), file, download_url);
            Ok(Box::new(dav_file) as Box<dyn DavFile>)
        }
        .boxed()
    }

    fn read_dir<'a>(
        &'a self,
        path: &'a DavPath,
        _meta: ReadDirMeta,
    ) -> FsFuture<FsStream<Box<dyn DavDirEntry>>> {
        debug!(path = %path.as_rel_ospath().display(), "fs: read_dir");
        async move {
            let files = self.read_dir_and_cache(path).await?;
            let mut v: Vec<Box<dyn DavDirEntry>> = Vec::with_capacity(files.len());
            for file in files {
                v.push(Box::new(file));
            }
            let stream = futures_util::stream::iter(v);
            Ok(Box::pin(stream) as FsStream<Box<dyn DavDirEntry>>)
        }
        .boxed()
    }

    fn metadata<'a>(&'a self, path: &'a DavPath) -> FsFuture<Box<dyn DavMetaData>> {
        debug!(path = %path.as_rel_ospath().display(), "fs: metadata");
        async move {
            let file = self.get_file(path).await?.ok_or(FsError::NotFound)?;
            Ok(Box::new(file) as Box<dyn DavMetaData>)
        }
        .boxed()
    }
}

#[derive(Debug, Clone)]
struct AliyunDavFile {
    drive: AliyunDrive,
    file: AliyunFile,
    current_pos: u64,
    download_url: Option<String>,
}

impl AliyunDavFile {
    fn new(drive: AliyunDrive, file: AliyunFile, download_url: Option<String>) -> Self {
        Self {
            drive,
            file,
            current_pos: 0,
            download_url,
        }
    }
}

impl DavFile for AliyunDavFile {
    fn metadata(&'_ mut self) -> FsFuture<'_, Box<dyn DavMetaData>> {
        debug!(file_id = %self.file.id, file_name = %self.file.name, "file: metadata");
        async move {
            let file = self.file.clone();
            Ok(Box::new(file) as Box<dyn DavMetaData>)
        }
        .boxed()
    }

    fn write_buf(&'_ mut self, _buf: Box<dyn Buf + Send>) -> FsFuture<'_, ()> {
        Box::pin(future::ready(Err(FsError::NotImplemented)))
    }

    fn write_bytes(&mut self, _buf: Bytes) -> FsFuture<()> {
        Box::pin(future::ready(Err(FsError::NotImplemented)))
    }

    fn read_bytes(&mut self, count: usize) -> FsFuture<Bytes> {
        debug!(
            file_id = %self.file.id,
            file_name = %self.file.name,
            pos = self.current_pos,
            count = count,
            size = self.file.size,
            "file: read_bytes",
        );
        async move {
            let download_url = self.download_url.as_ref().ok_or(FsError::NotFound)?;
            let content = self
                .drive
                .download(&self.file.id, download_url, self.current_pos, count)
                .await
                .map_err(|_| FsError::NotFound)?;
            self.current_pos += content.len() as u64;
            Ok(content)
        }
        .boxed()
    }

    fn seek(&mut self, pos: SeekFrom) -> FsFuture<u64> {
        debug!(
            file_id = %self.file.id,
            file_name = %self.file.name,
            pos = ?pos,
            "file: seek"
        );
        async move {
            let new_pos = match pos {
                SeekFrom::Start(pos) => pos,
                SeekFrom::End(pos) => (self.file.size as i64 - pos) as u64,
                SeekFrom::Current(size) => self.current_pos + size as u64,
            };
            self.current_pos = new_pos;
            Ok(new_pos)
        }
        .boxed()
    }

    fn flush(&mut self) -> FsFuture<()> {
        Box::pin(future::ready(Err(FsError::NotImplemented)))
    }
}
