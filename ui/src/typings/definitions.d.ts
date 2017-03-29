
declare interface Certificate {
    purpose: string;
    subject: string;
    not_before: Date;
    not_after: Date;
    fingerprint?: string;
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