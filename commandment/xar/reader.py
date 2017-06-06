import os
from typing import List
import zlib
from struct import *
from collections import namedtuple
import xml.etree.ElementTree as ET


class XarArchive(object):

    Header = Struct('>4sHHQQI')

    def __init__(self, path: str, toc: ET.Element, header=None):
        self.path = path
        self.toc = toc
        self.header = header

    @classmethod
    def load(cls, path: str) -> any:
        with open(path, 'rb') as fd:
            header = fd.read(28)  # The spec says the header must be at least 28
            if unpack('<4s', header) != 'xar!':
                raise ValueError('Not a XAR Archive')

            XarHeader = namedtuple('XarHeader', 'magic size version toc_len_compressed toc_len_uncompressed cksumalg')
            hdr = XarHeader._make(XarArchive.Header.unpack(header))

            toc_compressed = fd.read(hdr.toc_len_compressed)

        toc_uncompressed = zlib.decompress(toc_compressed)

        if len(toc_uncompressed) != hdr.toc_len_uncompressed:
            raise ValueError('Unexpected TOC Length does not match header')

        toc = ET.parse(toc_uncompressed)
        result = XarArchive(path, toc, header=hdr)

        return result

    def list(self, verbose: bool):
        for file in self.toc.iter('file'):
            print(file.findtext('name'))
