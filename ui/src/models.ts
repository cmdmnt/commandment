
export interface Profile {
    id?: number;
    description?: string;
    display_name?: string;
    expiration_date?: Date;
    identifier: string;
    organization?: string;
    uuid: string;
    removal_disallowed?: Boolean;
    version: number;
    scope?: string;
    removal_date?: Date;
    duration_until_removal?: number;
    consent_en?: string;
}


export interface Command {
    id?: number;
    command_class?: string;
    uuid?: string;
    input_data?: string;
    queued_status: string;
    queued_at?: Date;
    sent_at?: Date;
    acknowledged_at?: Date;
    after?: Date;
    ttl: number;
}


export interface Device {
    udid: string;
    build_version: string;
    device_name: string;
    model: string;
    model_name: string;
    os_version: string;
    product_name: string;
    serial_number: string;
    awaiting_configuration: boolean;
    last_seen: string;
    bluetooth_mac: string;
    wifi_mac: string;
    sip_enabled: boolean;
}

export interface DeviceGroup {
    id?: string;
    name: string;
}

export interface Organization {
    name: string;
    payload_prefix: string;
    x509_ou: string;
    x509_o: string;
    x509_st: string;
    x509_c: string;
}

export interface Certificate {
    type: string;
    x509_cn: string;
    not_before: Date;
    not_after: Date;
    fingerprint?: string;
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

export interface SCEPConfiguration {
    url: string;
    challenge_enabled: boolean;
    challenge: string;
    ca_fingerprint: string;
    subject: string;
    key_size: number;
    key_type: 'RSA';
    key_usage: any;
    subject_alt_name: string;
    retries: number;
    retry_delay: number;
    certificate_renewal_time_interval: number;
}
