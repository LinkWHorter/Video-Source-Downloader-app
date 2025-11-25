# 📹 VideoSourcer project for download any videos with open access! 📸

*A lightweight desktop tool for downloading videos from almost any website*

## 📸 Preview

<img width="893" height="507" alt="image" src="https://github.com/user-attachments/assets/a9b1d314-99f4-4d34-bb5a-e76b068afe8f" />

## 📘 Description

**VideoSourcer.exe** is a simple and fast video-downloading utility designed to save videos from a wide range of websites using only a link.
The program analyzes the provided URL, detects all available video qualities, and allows downloading from **144p up to 1080p** (depending on the source).

Built with a minimalistic UI and optimized for stable performance, VideoSourcer makes video saving convenient for everyday use.

## 🚀 Features

### ✔ Download videos from almost any website

Paste a link, choose quality, and download.
Supports platforms that allow direct video retrieval via accessible sources.

### ✔ Multiple quality options

Automatically detects available resolutions:

* **144p**
* **240p**
* **360p**
* **480p**
* **720p**
* **1080p**

*(Availability depends on the website and provided video stream.)*

### ✔ Clean and modern dark UI

The interface is optimized for simplicity:

* URL input field
* Format & resolution selector
* Progress bar
* One-click download button

### ✔ Local FFmpeg integration

VideoSourcer uses **FFmpeg** for merging and processing video/audio streams.
The program automatically looks for FFmpeg binaries inside:

```
%LOCALAPPDATA%/ffmpeg/
```

You only need to place your FFmpeg build in that folder before using the app.

## ⚙ Requirements

* **Windows 10/11**
* **FFmpeg** (must be located in `%LOCALAPPDATA%/ffmpeg/`)
* **Python 3.10+** (if running from source)

## 🖱 How to Use

1. Download ![icon](https://github.com/LinkWHorter/Video-Source-Downloader-app/blob/master/icons/icon.png) **[VideoSourcer.exe](https://github.com/LinkWHorter/Video-Source-Downloader-app/releases/download/videosourcer/VideoSourcer.exe)**
2. Launch ![icon](https://github.com/LinkWHorter/Video-Source-Downloader-app/blob/master/icons/icon.png) **VideoSourcer.exe** 
3. Insert a video link in the input field.
4. Select desired resolution.
5. Press **Download**.
6. Wait for processing — completed video files will appear in the application’s download directory.

## 📦 Installation

Simply download the latest release and run:

```
VideoSourcer.exe
```

No installation required.

## 🔧 Built With

* Python
* PyQt / Custom UI
* FFmpeg (external dependency)

## 📄 License

This project is distributed for educational and personal use.
