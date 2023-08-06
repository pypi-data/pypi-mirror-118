# pdfuris: extract URIs from PDF

pdfuris extracts URIs from a PDF and prints them to stdout.
It is most useful for getting a list of URIs to check validity before submitting a publication.

## Prerequisites

- Python >=3.6
- PyPDF2 (installed automatically by `pip`)

## Installation

```sh
python -m pip install pdfuris
```

Replace `python` with whatever command runs a version that is of Python 3.6 or greater.

## Usage

```
usage: pdfuris [-h] [--version] infile

Extract URIs from PDF.

positional arguments:
  infile      input PDF file

optional arguments:
  -h, --help  show this help message and exit
  --version   show program's version number and exit
```

## History

Derived from [`pdfcomments`](https://github.com/hoffmangroup/pdfcomments).

## License

GNU General Public License v3.

## Support

You are welcome to post issues but no guarantee of support is provided.
Pull requests are welcome.
