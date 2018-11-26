export interface Application {
    id?: string;
    itunes_store_id?: number;
    bundle_id?: string;
    purchase_method?: number;
    manifest_url: string;
    management_flags: number;
    change_management_state: "Managed" | null;
    display_name: string;
    description: string;
    version: string;
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

export interface InstalledPayload {
    id?: number;
    description: string;
    display_name: string;
    identifier: string;
    organization: string;
    payload_type: string;
    uuid: string;
}

export interface SCEPConfiguration {
    url: string;
    challenge_enabled: boolean;
    challenge: string;
    ca_fingerprint: string;
    subject: string;
    key_size: string; // Needs to be string to support redux-form
    key_type: "RSA";
    key_usage: string;
    subject_alt_name: string;
    retries: number;
    retry_delay: number;
    certificate_renewal_time_interval: number;
}

export interface VPPAccount {
    org_name: string;
    exp_date: string;
}
