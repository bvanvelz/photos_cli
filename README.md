# photos_cli
A CLI tool to manage photos.

## Install

    cd photos_cli
    python3 -m venv env
    source env/bin/activate
    pip install -r requirements.txt
    python photos_cli.py -h

## Usage

    photos_cli.py [-h] [--paths] [--duplicates] dir_path

    positional arguments:
      dir_path

    optional arguments:
      -h, --help        show this help message and exit
      --paths, -p       find photos in a directory
      --duplicates, -d  find duplicate photos
