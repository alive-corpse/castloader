#!/usr/bin/env python3

import sys
import feedparser
import curses
import requests
import os
import re
import time

def parse_feed(url):
    feed = feedparser.parse(url)
    return feed.entries

def download_file(url, filename, progress_callback, title):
    response = requests.get(url, stream=True)
    total_length = response.headers.get('content-length')
    if total_length is None:  # no content length header
        with open(filename, 'wb') as f:
            f.write(response.content)
    else:
        downloaded = 0
        total_length = int(total_length)
        with open(filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    progress_callback(downloaded, total_length)
        return downloaded, total_length

def strip_html(html):
    return re.sub('<.*?>', '', html)

def main(stdscr, url, save_path=None):
    entries = parse_feed(url)
    selected = []
    downloading = False
    progress = {}

    curses.curs_set(0)
    stdscr.nodelay(1)
    stdscr.timeout(100)

    current_page = 0
    page_size = 50
    total_pages = (len(entries) + page_size - 1) // page_size

    current_selection = 0

    def update_progress(entry, downloaded, total_length):
        progress[entry] = (downloaded, total_length)

    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, f"Page {current_page + 1}/{total_pages}")

        start = current_page * page_size
        end = start + page_size
        for i, entry in enumerate(entries[start:end], start=start + 1):
            prefix = ""
            if i - 1 == current_selection + start:
                prefix += "> "
            if entry in selected:
                prefix += "+ "
            if os.path.exists(os.path.join(save_path, os.path.basename(entry.links[1].href)) if save_path else os.path.basename(entry.links[1].href)):
                prefix += "+ "
            stdscr.addstr(i - start, 0, f"{prefix}{i}. {entry.title}")

        stdscr.addstr(page_size + 2, 0, "Commands: n - next page, p - previous page, up/down - navigate, s - select/deselect, a - select all on page, d - download, q - quit")

        if downloading:
            stdscr.clear()
            stdscr.addstr(0, 0, "Downloading...")
            for i, (entry, (downloaded, total_length)) in enumerate(progress.items()):
                downloaded_mb = downloaded / 1024 / 1024
                total_length_mb = total_length / 1024 / 1024
                if downloaded == total_length:
                    stdscr.addstr(i + 1, 0, f"{entry.title} ... Done: {downloaded_mb:.2f} MB / {total_length_mb:.2f} MB\n")
                else:
                    stdscr.addstr(i + 1, 0, f"{entry.title} ... ")
            stdscr.refresh()
            time.sleep(1)

            if all(downloaded == total_length for downloaded, total_length in progress.values()):
                stdscr.addstr(len(progress) + 1, 0, "All downloads completed. Press 'q' to quit or 'b' to go back to the list.")
                stdscr.refresh()
                while True:
                    key = stdscr.getch()
                    if key == ord('q'):
                        return
                    elif key == ord('b'):
                        downloading = False
                        current_page = 0
                        current_selection = 0
                        progress = {}
                        break

        key = stdscr.getch()

        if key == ord('n'):
            if current_page < total_pages - 1:
                current_page += 1
                current_selection = 0
        elif key == ord('p'):
            if current_page > 0:
                current_page -= 1
                current_selection = 0
        elif key == ord('s'):
            if entries[start + current_selection] in selected:
                selected.remove(entries[start + current_selection])
            else:
                selected.append(entries[start + current_selection])
        elif key == ord('d'):
            if not downloading:
                downloading = True
                progress = {}
                stdscr.clear()
                stdscr.addstr(0, 0, "Downloading...")
                stdscr.refresh()
                time.sleep(1)
                selected.reverse()  # Reverse the order of selected items
                for entry in selected:
                    url = entry.links[1].href
                    filename = os.path.basename(url)
                    full_path = os.path.join(save_path, filename) if save_path else filename
                    if not os.path.exists(full_path):
                        progress[entry] = (0, 0)
                        downloaded, total_length = download_file(url, full_path, lambda downloaded, total_length, entry=entry: update_progress(entry, downloaded, total_length), entry.title)
                        progress[entry] = (downloaded, total_length)
        elif key == ord('q'):
            break
        elif key == ord('a'):
            for entry in entries[start:end]:
                if entry not in selected:
                    selected.append(entry)
        elif key == curses.KEY_UP:
            if current_selection > 0:
                current_selection -= 1
        elif key == curses.KEY_DOWN:
            if current_selection < min(page_size - 1, len(entries) - start - 1):
                current_selection += 1

if __name__ == "__main__":
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Usage: python castloader.py <feed_url> [save_path]")
        sys.exit(1)

    url = sys.argv[1]
    save_path = sys.argv[2] if len(sys.argv) == 3 else None

    if save_path:
        if save_path.startswith('/'):
            full_path = save_path
        else:
            full_path = os.path.join(os.getcwd(), save_path)

        if not os.path.exists(full_path):
            try:
                os.makedirs(full_path)
            except Exception as e:
                print(f"Failed to create directory {full_path}: {e}")
                sys.exit(1)
    else:
        full_path = None

    curses.wrapper(main, url, full_path)
