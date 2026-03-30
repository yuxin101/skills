# Changelog

## v3.0.1 (2026-03-26)

### Fixed
- **Filename cleaning**: Removes all punctuation marks, emojis, and special characters from filenames
- **Chinese punctuation**: Proper handling of Chinese punctuation marks (【】·、，。！？《》：；等)
- **Emoji removal**: Removes all emojis and special Unicode characters
- **S3 compatibility**: Ensures clean filenames for better S3 compatibility

### Technical Details
- Enhanced regex patterns for comprehensive character removal
- Extended Unicode range for emoji detection (U+1F300 to U+1F9FF)
- Maintains Chinese characters, letters, numbers, and spaces
- Preserves readability while removing clutter

## v3.0.0 (2026-03-25)

### Added
- **Universal video downloader**: Supports YouTube, Twitter/X, TikTok, Douyin, Bilibili, and 1000+ websites via yt-dlp
- **Platform detection**: Automatically detects video platform
- **New command**: `video-to-s3-universal.js` for universal video downloading
- **Backward compatibility**: `youtube-to-s3.js` still works for YouTube-specific use

### Changed
- **Complete rewrite**: From YouTube-specific to universal video downloader
- **Improved architecture**: Better separation of concerns
- **Enhanced error handling**: More robust error recovery

## v2.0.0 (2026-03-25)

### Added
- **S3 Multipart Upload**: Uses multipart upload for all file sizes
- **Memory optimization**: Chunked reading to avoid memory overflow
- **Error recovery**: Automatic retry mechanism
- **Smart chunk sizing**: Adjusts based on file size

### Fixed
- **Help system**: Proper `--help` display
- **Consistent API**: Always uses multipart upload
- **Cleaner codebase**: Removed compatibility layers

## v1.0.0 (2026-03-25)

### Initial Release
- Basic YouTube video download and S3 upload
- Simple PUT upload for small files
- Foundation for future improvements

## 3.0.2 (2026-03-26)

### 🐛 Bug 修复
- **文件名处理**: 修复文件名中的空白字符问题
  - 之前：合并多个空格为单个空格
  - 现在：移除所有空白字符（包括空格）
  - 影响文件：`video-to-s3-universal.js`, `youtube-to-s3.js`
  
### 🔧 技术改进
- 保持硬编码路径配置，不依赖系统环境变量
- 确保文件名生成的一致性

