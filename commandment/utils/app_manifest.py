import subprocess
from tempfile import mkdtemp
import os
from xml.dom.minidom import parse, parseString
from hashlib import md5
import plistlib

# use system PATH
XAR_PATH = 'xar'

MD5_CHUNK_SIZE = 1024 * 1024 * 10 # 10 MiB

def pkg_signed(filename):
	xar_args = [XAR_PATH,
		'-t', # only test archive
		'--dump-toc=-',
		'-f',
		filename]

	p = subprocess.Popen(xar_args, stdout=subprocess.PIPE)
	toc, _ = p.communicate()

	if p.returncode != 0:
		return False

	toc_md = parseString(toc)

	# for purposes of checking just see if the xar TOC has an X509Certificate element
	return len(toc_md.getElementsByTagName('X509Certificate')) > 0

def get_pkg_bundle_ids(filename):
	'''Get metadata from Distribution or PackageInfo inside of pkg'''

	tmp_dir = mkdtemp()

	print 'Extracting Distribution/PackageInfo file to', tmp_dir

	xar_args = [XAR_PATH,
		'-x', # extract switch
		'--exclude', '/', # exclude any files in subdirectories
		'-C', tmp_dir, # extract to our temporary directory
		'-f', filename, # extract this specific file
		'Distribution', 'PackageInfo'] # files to extract

	rtn = subprocess.call(xar_args)

	tmp_dist_file = os.path.join(tmp_dir, 'Distribution')
	tmp_pinf_file = os.path.join(tmp_dir, 'PackageInfo')

	pkgs = []
	bundles = []

	# for non-PackageInfo packages (use PackageInfo)
	if os.path.exists(tmp_dist_file):
		# use XML minidom to parse a Distribution file
		dist_md = parse(tmp_dist_file)

		# capture the pkg IDs and versions by searching for 'pkg-ref' elements
		# which include a 'version' attribute on them. append them to our list
		for i in dist_md.getElementsByTagName('pkg-ref'):
			if i.hasAttribute('version'):
				pkgs.append((i.getAttribute('id'), i.getAttribute('version')))

		# capture the bundle IDs and versions by searching for 'bundle'
		# elements which we're searching for a 'CFBundleVersion' attribute on
		# them. append them to our list
		for i in dist_md.getElementsByTagName('bundle'):
			bundles.append((i.getAttribute('id'), i.getAttribute('CFBundleVersion')))

		print 'Removing Distribution file'
		os.unlink(tmp_dist_file)

	# for non-Distribution packages (use the PackageInfo)
	if os.path.exists(tmp_pinf_file):
		pinf_md = parse(tmp_pinf_file)

		# capture the pkg ID and version by searching for a pkg-info element
		# and using the identifier and version attributes
		for i in pinf_md.getElementsByTagName('pkg-info'):
			pkgs.append((i.getAttribute('identifier'), i.getAttribute('version')))

		print 'Removing PackageInfo file'
		os.unlink(tmp_pinf_file)

	
	print 'Removing temp directory'
	os.rmdir(tmp_dir)

	return (pkgs, bundles)

def get_chunked_md5(filename, chunksize=MD5_CHUNK_SIZE):
	h = md5()
	md5s = []
	total_hash = md5()
	with open(filename, 'rb') as f:
		for chunk in iter(lambda: f.read(chunksize), b''):
			new_hash = md5()
			new_hash.update(chunk)
			total_hash.update(chunk)
			md5s.append(new_hash.hexdigest())

	return (total_hash.hexdigest(), md5s)
