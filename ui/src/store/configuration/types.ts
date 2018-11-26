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
