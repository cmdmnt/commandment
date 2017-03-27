
declare interface Certificate {
    cert_type: string;
    subject: string;
    not_before: Date;
    not_after: Date;
    fingerprint?: string;
}