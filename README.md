# CastLoader

---
For the Russian version of this README, please refer to the [README\_RUS.md](README\_RUS.md) file in this directory.
---


CastLoader is a command-line tool for downloading podcasts from RSS feeds. The project allows users to browse a list of podcasts, select the ones they want to download, and save them to a specified directory.

The project was created for downloading podcasts to MP3 players that often sort podcasts not by file name, but by file creation date. Therefore, the selected files are downloaded in single-threaded mode and in the order of release. That is, the oldest podcast from the selected ones will be downloaded first, then the newer ones, and so on up to the most recent.

## Features

- Browse a list of podcasts from an RSS feed.
- Select podcasts for download.
- Download podcasts to a specified directory.
- Interactive interface using the `curses` library.

## Requirements

- Python 3.6 or higher
- Libraries: `feedparser`, `requests`, `curses`

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/CastLoader.git
   cd CastLoader
   ```

2. Install the required dependencies:
   ```bash
   pip3 install -r requirements.txt
   ```

## Usage

Run the script with the RSS feed URL and, optionally, the path to save the podcasts:

```bash
python castloader.py <feed_url> [save_path]
```

The path can be either relative or absolute.

### Examples

1. Download podcasts from a feed and save them to the current directory:
   ```bash
   python castloader.py http://example.com/podcast/feed
   ```

2. Download podcasts from a feed and save them to a specified directory:
   ```bash
   python castloader.py http://example.com/podcast/feed /path/to/save/podcasts
   ```

## Interface Commands

- `n` - Next page
- `p` - Previous page
- `↑`/`↓` - Navigate up/down
- `s` - Select/deselect a podcast
- `a` - Select all podcasts on the current page
- `d` - Start downloading selected podcasts
- `q` - Quit the program

## License

This project is licensed under the [MIT License](LICENSE).

## Authors

- Evgeniy Shumilov <evgeniy.shumilov@gmail.com>


