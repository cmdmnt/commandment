export const JSONAPI_HEADERS = {
    'Content-Type': 'application/vnd.api+json',
    'Accept': 'application/vnd.api+json'
};

export const JSON_HEADERS = {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
};

export type CertificatePurpose = 'apns' | 'ssl';

// Flask-REST-JSONAPI Filter and Sort definitions


export type FlaskFilterOperation = 'any' | 'between' | 'endswith' | 'eq' | 'ge' | 'gt' |
    'has' | 'ilike' | 'in_' | 'is_' | 'isnot' | 'like' | 'le' | 'lt' | 'match' | 'ne' | 'notlike' |
    'notin_' | 'notlike' | 'startswith';

export interface FlaskFilter {
    name: string;
    op: FlaskFilterOperation;
    val?: string;
    field?: string;
}

export type FlaskFilters = Array<FlaskFilter>;

export interface OtherAction {
    type: string;
    payload?: any;
}