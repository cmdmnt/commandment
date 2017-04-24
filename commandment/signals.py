from blinker import Namespace
signals = Namespace()

# Sent when a device enrolls for the first time, or re-enrols after checking out
device_enrolled = signals.signal('device-enrolled')

# Sent when a device voluntarily checks out
device_unenrolled = signals.signal('device-unenrolled')

