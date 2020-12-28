# photos_cli
A CLI tool to manage photos.

## Install

    python3 -m venv env
    source env/bin/activate
    pip install -r requirements.txt
    python photos_cli.py -h

## Usage

    photos_cli.py [-h] [--list DIR_PATH] [--duplicates DIR_PATH]

    optional arguments:
      -h, --help            show this help message and exit
      --list DIR_PATH       Find photos in a directory
      --duplicates DIR_PATH
                            Find duplicate photos