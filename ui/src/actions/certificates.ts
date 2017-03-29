/// <reference path="../typings/redux-api-middleware.d.ts" />
import { CALL_API, RSAA } from 'redux-api-middleware';
import {JSONAPI_HEADERS, FlaskFilters, FlaskFilter} from './constants'

export type INDEX_REQUEST = 'certificates/INDEX_REQUEST';
export const INDEX_REQUEST: INDEX_REQUEST = 'certificates/INDEX_REQUEST';
export type INDEX_SUCCESS = 'certificates/INDEX_SUCCESS';
export const INDEX_SUCCESS: INDEX_SUCCESS = 'certificates/INDEX_SUCCESS';
export type INDEX_FAILURE = 'certificates/INDEX_FAILURE';
export const INDEX_FAILURE: INDEX_FAILURE = 'certificates/INDEX_FAILURE';

export interface IndexActionRequest {
    (size?: number, number?: number, sort?: Array<string>, filter?: Array<FlaskFilter>): RSAA<INDEX_REQUEST, INDEX_SUCCESS, INDEX_FAILURE>;
}

export interface IndexActionResponse {
    type: INDEX_REQUEST | INDEX_FAILURE | INDEX_SUCCESS;
    payload?: JSONAPIListResponse<JSONAPIObject<Certificate>>;
}

export const index: IndexActionRequest = (
    size: number = 50,
    number: number = 1,
    sort: Array<string> = [],
    filter?: Array<FlaskFilter>
): RSAA<INDEX_REQUEST, INDEX_SUCCESS, INDEX_FAILURE> => {

    let queryParameters = [];
    queryParameters.push(`size=${size}`);
    queryParameters.push(`number=${number}`);

    if (sort.length > 0) {
        // TODO: sorting
    }

    if (filter && filter.length > 0) {
        let rawFilters = JSON.stringify(filter);
        queryParameters.push(`filter=${rawFilters}`);
    }

    return {
        [CALL_API]: {
            endpoint: '/api/v1/certificates/?' + queryParameters.join('&'),
            method: 'GET',
            types: [
                INDEX_REQUEST,
                INDEX_SUCCESS,
                INDEX_FAILURE
            ],
            headers: JSONAPI_HEADERS
        }
    }
};

export type PUSHCERT_REQUEST = 'certificates/PUSHCERT_REQUEST';
export const PUSHCERT_REQUEST: PUSHCERT_REQUEST = 'certificates/PUSHCERT_REQUEST';
export type PUSHCERT_SUCCESS = 'certificates/PUSHCERT_SUCCESS';
export const PUSHCERT_SUCCESS: PUSHCERT_SUCCESS = 'certificates/PUSHCERT_SUCCESS';
export type PUSHCERT_FAILURE = 'certificates/PUSHCERT_FAILURE';
export const PUSHCERT_FAILURE: PUSHCERT_FAILURE = 'certificates/PUSHCERT_FAILURE';

export interface FetchPushCertificateActionRequest {
    (): RSAA<PUSHCERT_REQUEST, PUSHCERT_SUCCESS, PUSHCERT_FAILURE>;
}

export interface FetchPushCertificateActionResponse {
    type: PUSHCERT_REQUEST | PUSHCERT_SUCCESS | PUSHCERT_FAILURE;
    payload?: JSONAPIDetailResponse<Certificate>;
}

export const fetchPushCertificate: FetchPushCertificateActionRequest = (): RSAA<PUSHCERT_REQUEST, PUSHCERT_SUCCESS, PUSHCERT_FAILURE> => {
    return {
        [CALL_API]: {
            endpoint: '/api/v1/push_certificate',
            method: 'GET',
            types: [
                PUSHCERT_REQUEST,
                PUSHCERT_SUCCESS,
                PUSHCERT_FAILURE
            ],
            headers: JSONAPI_HEADERS
        }
    }
};

export type CERTTYPE_REQUEST = 'certificates/CERTTYPE_REQUEST';
export const CERTTYPE_REQUEST: CERTTYPE_REQUEST = 'certificates/CERTTYPE_REQUEST';
export type CERTTYPE_SUCCESS = 'certificates/CERTTYPE_SUCCESS';
export const CERTTYPE_SUCCESS: CERTTYPE_SUCCESS = 'certificates/CERTTYPE_SUCCESS';
export type CERTTYPE_FAILURE = 'certificates/CERTTYPE_FAILURE';
export const CERTTYPE_FAILURE: CERTTYPE_FAILURE = 'certificates/CERTTYPE_FAILURE';

export interface FetchCertificateTypeActionRequest {
    (certType: string): RSAA<CERTTYPE_REQUEST, CERTTYPE_SUCCESS, CERTTYPE_FAILURE>;
}

export interface FetchCertificateTypeActionResponse {
    type: CERTTYPE_REQUEST | CERTTYPE_SUCCESS | CERTTYPE_FAILURE;
    payload?: JSONAPIDetailResponse<Certificate>;
}


export const fetchCertificatesForType: FetchCertificateTypeActionRequest = (certType: string): RSAA<CERTTYPE_REQUEST, CERTTYPE_SUCCESS, CERTTYPE_FAILURE> => {
    return {
        [CALL_API]: {
            endpoint: `/api/v1/certificates/type/${certType}`,
            method: 'GET',
            types: [
                CERTTYPE_REQUEST,
                CERTTYPE_SUCCESS,
                CERTTYPE_FAILURE
            ],
            headers: JSONAPI_HEADERS
        }
    }
};