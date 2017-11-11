import argparse
from typing import List, Tuple, Optional
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


def url_from_metadata(path: str) -> Optional[str]:
    """Try to determine the download URL from the spotlight attributes if the local machine is a mac."""
    try:
        from Foundation import NSFileManager, NSPropertyListSerialization
    except:
        return None

    fm = NSFileManager.defaultManager()
    attrs, err = fm.attributesOfItemAtPath_error_(path, None)
    if err:
        return None

    if 'NSFileExtendedAttributes' not in attrs:
        return None

    extd_attrs = attrs['NSFileExtendedAttributes']

    if 'com.apple.metadata:kMDItemWhereFroms' not in extd_attrs:
        return None
    else:
        plist_data: bytes = extd_attrs['com.apple.metadata:kMDItemWhereFroms']
        value: List[str] = plistlib.loads(plist_data)
        if len(value) > 0:
            return value.pop(0)
        else:
            return None


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

    url = url_from_metadata(args.source)

    manifest = {
        'items': [{
            'assets': [{
                'kind': 'software-package',
                'md5-size': MD5_CHUNK_SIZE,
                'md5s': chunks,
                'url': '{}'.format(url) if url else 'https://package/url/here.pkg'
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
    manifest['items'][0]['metadata'].update(pkgs_bundles[0])

    if len(bundles) > 1:
        manifest['items'][0]['metadata']['items'] = [{'bundle-identifier': i[0], 'bundle-version': i[1]} for i in bundles]

    print(plistlib.dumps(manifest).decode('utf8'))

