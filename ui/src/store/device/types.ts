// Valid JSON-API relationships
export type DeviceRelationship = "commands" | "tags" | "groups" | "profiles";

export interface Device {
    udid: string;
    // topic
    last_seen: string;
    is_enrolled: boolean;
    build_version: string;
    device_name: string;
    model: string;
    model_name: string;
    os_version: string;
    product_name: string;
    serial_number: string;
    hostname: string;
    local_hostname: string;
    available_device_capacity: number;
    device_capacity: number;
    wifi_mac: string;
    bluetooth_mac: string;
    awaiting_configuration: boolean;
    // push_magic
    // tokenupdate_at
    // last_apns_id

    // last_push_at
    passcode_present: boolean;
    passcode_compliant: boolean;
    passcode_compliant_with_profiles: boolean;
    fde_enabled: boolean;
    fde_has_prk: boolean;
    fde_has_irk: boolean;
    firewall_enabled: boolean;
    block_all_incoming: boolean;
    stealth_mode_enabled: boolean;
    sip_enabled: boolean;
    battery_level: number;
    carrier_settings_version: string;
    cellular_technology: string;
    current_carrier_network: string;
    current_mcc: string;
    current_mnc: string;
    data_roaming_enabled: boolean;
    eas_device_identifier: string;
    iccid: string;
    imei: string;
    is_activation_lock_enabled: boolean;
    is_cloud_backup_enabled: boolean;
    is_device_locator_service_enabled: boolean;
    is_do_not_disturb_in_effect: boolean;
    is_mdm_lost_mode_enabled: boolean;
    is_roaming: boolean;
    is_supervised: boolean;
    itunes_store_account_hash: string;
    itunes_store_account_is_active: boolean;
    last_cloud_backup_date: string;
    maximum_resident_users: number;
    meid: string;
    modem_firmware_version: string;
    passcode_lock_grace_period_enforced: number;
    personal_hotspot_enabled: boolean;
    phone_number: string;
    sim_carrier_network: string;
    subscriber_carrier_network: string;
    subscriber_mcc: string;
    subscriber_mnc: string;
    voice_roaming_enabled: boolean;

    // DEP
    dep_profile_id?: number;
    description?: string;
    asset_tag?: string;
    color?: string;
    device_assigned_by?: string;
    device_assigned_date?: string;
    device_family?: string;
    is_dep: boolean;
    os?: string;
    profile_assign_time?: string;
    profile_push_time?: string;
    profile_status?: string;
    profile_uuid?: string;
}

export interface InstalledCertificate {
    x509_cn: string;
    is_identity: boolean;
    fingerprint_sha256: string;
}

export interface InstalledApplication {
    id?: number;
    device_udid: string;
    device_id: number;
    bundle_identifier: string;
    version: string;
    short_version: string;
    name: string;
    bundle_size: number;
    dynamic_size: number;
    is_validated: boolean;
}

export interface InstalledProfile {
    id?: number;
    device_udid: string;
    device_id: number;
    has_removal_password: boolean;
    is_encrypted: boolean;
    payload_description: string;
    payload_display_name: string;
    payload_identifier: string;
    payload_organization: string;
    payload_removal_disallowed: boolean;
    payload_uuid: string;
}

export interface AvailableOSUpdate {
    id?: string;
    allows_install_later: boolean;
    app_identifiers_to_close: string[];
    human_readable_name: string;
    human_readable_name_locale: string;
    is_config_data_update: boolean;
    is_critical: boolean;
    is_firmware_update: boolean;
    metadata_url: string;
    product_key: string;
    restart_required: boolean;
    version: string;
}

export enum MDMCommandType {
    CertificateList = "CertificateList",
    ClearPasscode = "ClearPasscode",
    DeviceInformation = "DeviceInformation",
    DeviceLock = "DeviceLock",
    InstalledApplicationList = "InstalledApplicationList",
    InstallProfile = "InstallProfile",
    InstallProvisioningProfile = "InstallProvisioningProfile",
    ProfileList = "ProfileList",
    ProvisioningProfileList = "ProvisioningProfileList",
    RemoveProfile = "RemoveProfile",
    RemoveProvisioningProfile = "RemoveProvisioningProfile",
    RestartDevice = "RestartDevice",
    SecurityInfo = "SecurityInfo",
    ShutDownDevice = "ShutDownDevice",
}

export interface Command {
    id?: number;
    command_class?: MDMCommandType;
    uuid?: string;
    input_data?: string;
    queued_status: string;
    queued_at?: Date;
    sent_at?: Date;
    acknowledged_at?: Date;
    after?: Date;
    ttl: number;
}

export enum DeviceModelName {
    iPad = "iPad",
    iPhone = "iPhone",
    MacMini = "Mac Mini",
    MacPro = "Mac Pro",
}

export enum DeviceOperatingSystem {
    iOS = "iOS",
    macOS = "macOS",
    tvOS = "tvOS",
    watchOS = "watchOS",
    Unknown = "Unknown",
}

export function operatingSystem(model: DeviceModelName): DeviceOperatingSystem {
    switch (model) {
        case DeviceModelName.iPad:
        case DeviceModelName.iPhone:
            return DeviceOperatingSystem.iOS;
        case DeviceModelName.MacMini:
        case DeviceModelName.MacPro:
            return DeviceOperatingSystem.macOS;
        default:
            return DeviceOperatingSystem.Unknown;
    }
}
