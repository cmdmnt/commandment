
declare interface Certificate {
    purpose: string;
    subject: string;
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