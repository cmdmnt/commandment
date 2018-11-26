export interface Certificate {
    type: string;
    x509_cn: string;
    not_before: Date;
    not_after: Date;
    fingerprint?: string;
}
