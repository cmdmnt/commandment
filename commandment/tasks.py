"""mdm app module: Controller logic for MDM Blueprint"""

import logging
from .models import Profile, ProfileStatus, Device
from .database import db_session
from .push import push_to_device
from .profiles.service import ProfileService
from .mdm import device as mdm_device

__author__ = "Phil Weir <phil.weir@flaxandteal.co.uk>"

# In a future iteration, this would raise an event to which subscribers could subscribe
def process_profile_deployment_change(profile_id):
    """Push commands to action installation and removal to device"""

    profile = db_session.query(Profile).get(profile_id)
    profile_service = ProfileService()

    if profile.status == ProfileStatus.PENDING_INSTALLATION:
        target = ProfileStatus.ACTIVE
        finalize = profile_service.finalize_installation
    elif profile.status in (ProfileStatus.PENDING_REMOVAL, ProfileStatus.PENDING_DELETION):
        finalize = profile_service.finalize_removal
        if profile.status == ProfileStatus.PENDING_REMOVAL:
            target = ProfileStatus.INACTIVE
        else:
            target = ProfileStatus.PENDING_DELETION
    else:
        return

    affected_devices = set()

    for group in profile.mdm_groups:
        affected_devices |= set(group.devices)

    logging.info("Updating status for %s devices in %s groups", len(affected_devices), len(profile.mdm_groups))

    for device in affected_devices:
        finalize(profile, device)

    db_session.commit()

    for device in affected_devices:
        push_to_device(device)

    profile.status = target
    db_session.commit()

def process_enrolment_complete(device_id, awaiting):
    device = db_session.query(Device).get(device_id)
    print device
    mdm_device.device_first_post_enroll(device, awaiting)
