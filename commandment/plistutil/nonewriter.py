from io import BytesIO
from plistlib import _PlistWriter, FMT_XML, _FORMATS


class PlistNoneWriter(_PlistWriter):
    """This subclass of PlistWriter writes out XML formatted property lists, but specifically skips any key for which
    its value is **None**."""

    def write_dict(self, d):
        if d:
            self.begin_element("dict")
            if self._sort_keys:
                items = sorted(d.items())
            else:
                items = d.items()

            for key, value in items:
                if not isinstance(key, str):
                    if self._skipkeys:
                        continue
                    raise TypeError("keys must be strings")

                if value is None:
                    continue
                    
                self.simple_element("key", key)
                self.write_value(value)
            self.end_element("dict")

        else:
            self.simple_element("dict")


# These methods are copied here for convenience

def dump(value, fp, *, fmt=FMT_XML, sort_keys=True, skipkeys=False):
    """Write 'value' to a .plist file. 'fp' should be a (writable)
    file object.
    """
    if fmt not in _FORMATS:
        raise ValueError("Unsupported format: %r"%(fmt,))

    writer = PlistNoneWriter(fp, sort_keys=sort_keys, skipkeys=skipkeys)
    writer.write(value)


def dumps(value, *, fmt=FMT_XML, skipkeys=False, sort_keys=True):
    """Return a bytes object with the contents for a .plist file.
    """
    fp = BytesIO()
    dump(value, fp, fmt=fmt, skipkeys=skipkeys, sort_keys=sort_keys)
    return fp.getvalue()
