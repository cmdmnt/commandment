
declare interface Profile {
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


declare interface Command {
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


declare interface Device {
    udid: string;
    build_version: string;
    device_name: string;
    model: string;
    model_name: string;
    os_version: string;
    product_name: string;
    serial_number: string;
    awaiting_configuration: boolean;
}

declare interface Organization {
    name: string;
    payload_prefix: string;
    x509_ou: string;
    x509_o: string;
    x509_st: string;
    x509_c: string;
}

declare interface Certificate {
    type: string;
    x509_cn: string;
    not_before: Date;
    not_after: Date;
    fingerprint?: string;
}

declare interface MDMConfig {
    prefix: string;
    addl_config: string;
    topic: string;
    access_rights: number;
    mdm_url: string;
    checkin_url: string;
    mdm_name: string;
    description: string;
    ca_cert_id: number;
    push_cert_id: number;
    device_identity_method: string;
    scep_url: string;
    scep_challenge: string;
}

declare interface JSONAPIObject<TObject> {
    id: string|number;
    type: string;
    attributes: TObject;
    relationships: Array<any>;
    links?: {
        self?: string;
    }
}

interface JSONAPIDetailResponse<TObject> {
    data?: JSONAPIObject<TObject>;
    links?: {
        self?: string;
    },
    meta?: {
        count?: number;
    }
    jsonapi: {
        version: string;
    }
}

interface JSONAPIListResponse<TObject> {
    data?: Array<TObject>;
    links?: {
        self?: string;
    },
    meta?: {
        count?: number;
    }
    jsonapi: {
        version: string;
    }
}