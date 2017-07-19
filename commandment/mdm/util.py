from commandment.mdm import commands
from commandment.models import db, Device, Command


def queryresponses_to_query_set(responses: dict):
    return {commands.DeviceInformation.Queries(k): v for k, v in responses.items()}


def queue_full_inventory(device: Device):
    """Enqueue all inventory commands for a device.

    Typically run at first check-in

    Args:
          device (Device): The device
    """
    # DeviceInformation
    di = commands.DeviceInformation.for_platform(device.platform, device.os_version)
    db_command = Command.from_model(di)
    db_command.device = device
    db.session.add(db_command)

    # InstalledApplicationList - Pretty taxing so don't run often
    ial = commands.InstalledApplicationList()
    db_command_ial = Command.from_model(ial)
    db_command_ial.device = device
    db.session.add(db_command_ial)

    # CertificateList
    cl = commands.CertificateList()
    dbc = Command.from_model(cl)
    dbc.device = device
    db.session.add(dbc)

    # SecurityInfo
    si = commands.SecurityInfo()
    dbsi = Command.from_model(si)
    dbsi.device = device
    db.session.add(dbsi)

    # ProfileList
    pl = commands.ProfileList()
    db_pl = Command.from_model(pl)
    db_pl.device = device
    db.session.add(db_pl)

    # AvailableOSUpdates
    au = commands.AvailableOSUpdates()
    au_pl = Command.from_model(au)
    au_pl.device = device
    db.session.add(au_pl)

    db.session.commit()
