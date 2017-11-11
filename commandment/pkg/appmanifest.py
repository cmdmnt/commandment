import argparse
from typing import List, Tuple
from bixar.archive import XarFile
from xml.etree import ElementTree
import plistlib
import hashlib
import os.path

Packages = List[Tuple[str, str]]
Bundles = List[Tuple[str, str]]
MD5_CHUNK_SIZE = 10 << 20


def blow_chunks(fileobj) -> Tuple[str, List[str]]:
    fileobj.seek(0)
    chunks = []
    total_hash = hashlib.md5()
    
    for chunk in iter(lambda: fileobj.read(MD5_CHUNK_SIZE), b''):
        new_hash = hashlib.md5()
        new_hash.update(chunk)
        total_hash.update(chunk)
        chunks.append(new_hash.hexdigest())

    return total_hash.hexdigest(), chunks


def main():
    parser = argparse.ArgumentParser(description='Create an application manifest')
    parser.add_argument('source',
                        help='Source pkg [REQUIRED!]',
                        metavar='filename')
    parser.add_argument('-u',
                        help='url prefix, for where the package will be downloaded from. package name will be appended')

    args = parser.parse_args()

    archive = XarFile(path=args.source)
    distribution = archive.extract_bytes('Distribution')
    package_info = archive.extract_bytes('PackageInfo')
    packages: Packages = []
    bundles: Bundles = []
    file_size = os.path.getsize(args.source)

    if distribution:
        el = ElementTree.fromstring(distribution)
        for pkgRef in el.iter('pkg-ref'):
            if 'version' in pkgRef.attrib:
                packages.append((pkgRef.attrib['id'], pkgRef.attrib['version']))

        bundles = [(b.attrib['id'], b.attrib['CFBundleVersion']) for b in el.iter('bundle')]

    if package_info:
        el = ElementTree.fromstring(package_info)
        for pkgInfo in el.iter('pkg-info'):
            packages.append((pkgInfo.attrib['identifier'], pkgInfo.attrib['version']))

    with open(args.source, 'rb') as fd:
        total_hash, chunks = blow_chunks(fd)

    manifest = {
        'items': [{
            'assets': [{
                'kind': 'software-package',
                'md5-size': MD5_CHUNK_SIZE,
                'md5s': chunks,
                'url': '{}{}'.format(args.u, os.path.basename(args.source)) if args.u else 'https://package/url/here.pkg'
            }],
            'metadata': {
                'kind': 'software',
                'title': os.path.basename(args.source),
                'sizeInBytes': file_size,
                'bundle-identifier': '',
                'bundle-version': ''
            }
        }]
    }

    pkgs_bundles = [{'bundle-identifier': i[0], 'bundle-version': i[1]} for i in packages]
    manifest['metadata'].update(pkgs_bundles[0])

    if len(bundles) > 1:
        manifest['metadata']['items'] = [{'bundle-identifier': i[0], 'bundle-version': i[1]} for i in bundles]

    print(plistlib.dumps(manifest).decode('utf8'))

