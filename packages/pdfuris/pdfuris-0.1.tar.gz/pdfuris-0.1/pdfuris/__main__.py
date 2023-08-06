#!/usr/bin/env python
"""__main__.py: Extract URIs from PDF."""

__version__ = "0.1"

# Copyright 2018-2021 Michael M. Hoffman <michael.hoffman@utoronto.ca>

from argparse import Namespace
import sys
from typing import Iterator, List

from PyPDF2 import PdfFileReader
from PyPDF2.pdf import PageObject

try:
    from os import EX_OK
except ImportError:
    EX_OK = 0

# monkey-patching to fix
# https://github.com/mstamy2/PyPDF2/issues/151
from PyPDF2 import generic

PDF_DOC_ENCODING = list(generic._pdfDocEncoding)
PDF_DOC_ENCODING[9] = "\u0009"
PDF_DOC_ENCODING[10] = "\u000a"
PDF_DOC_ENCODING[13] = "\u000d"

generic._pdfDocEncoding = tuple(PDF_DOC_ENCODING)

ENCODING = "utf-8"

STRICT = False


def iter_annot_uris(page: PageObject) -> Iterator[str]:
    try:
        annot_indirects = page["/Annots"]
    except KeyError:
        return

    for annot_indirect in annot_indirects:
        annot = annot_indirect.getObject()

        # PDF 1.7 s12.5.6.5 Link Annotations
        if annot["/Subtype"] != "/Link":
            continue

        # PDF 1.7 s12.6 Actions
        try:
            action = annot["/A"]
        except KeyError:
            continue

        if action["/S"] == "/URI":
            yield action["/URI"]


def load_uris(filename: str) -> Iterator[str]:
    reader = PdfFileReader(filename, STRICT)
    for page in reader.pages:
        for uri in iter_annot_uris(page):
            yield uri


def write_uris(uris: Iterator[str]) -> None:
    for uri in uris:
        print(uri)


def pdfuris(infilename: str) -> int:
    uris = load_uris(infilename)

    write_uris(uris)

    return EX_OK


def parse_args(args: List[str]) -> Namespace:
    from argparse import ArgumentParser

    description = __doc__.splitlines()[0].partition(": ")[2]
    parser = ArgumentParser(description=description)
    parser.add_argument("infile", help="input PDF file")

    version = f"%(prog)s {__version__}"
    parser.add_argument("--version", action="version", version=version)

    return parser.parse_args(args)


def main(argv: List[str] = sys.argv[1:]) -> int:
    args = parse_args(argv)

    return pdfuris(args.infile)


if __name__ == "__main__":
    sys.exit(main())
