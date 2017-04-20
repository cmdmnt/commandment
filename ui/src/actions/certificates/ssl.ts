/// <reference path="../../typings/redux-api-middleware.d.ts" />
import { CALL_API, RSAA } from 'redux-api-middleware';
import {JSONAPI_HEADERS, FlaskFilters, FlaskFilter} from '../constants'


export type SSLCERT_REQUEST = 'certificates/SSLCERT_REQUEST';
export const SSLCERT_REQUEST: SSLCERT_REQUEST = 'certificates/SSLCERT_REQUEST';
export type SSLCERT_SUCCESS = 'certificates/SSLCERT_SUCCESS';
export const SSLCERT_SUCCESS: SSLCERT_SUCCESS = 'certificates/SSLCERT_SUCCESS';
export type SSLCERT_FAILURE = 'certificates/SSLCERT_FAILURE';
export const SSLCERT_FAILURE: SSLCERT_FAILURE = 'certificates/SSLCERT_FAILURE';

export interface FetchSSLCertificatesActionRequest {
    (): RSAA<SSLCERT_REQUEST, SSLCERT_SUCCESS, SSLCERT_FAILURE>;
}

export interface FetchSSLCertificatesActionResponse {
    type: SSLCERT_REQUEST | SSLCERT_SUCCESS | SSLCERT_FAILURE;
    payload?: JSONAPIListResponse<JSONAPIObject<Certificate>>;
}

export const fetchSSLCertificates: FetchSSLCertificatesActionRequest = (): RSAA<SSLCERT_REQUEST, SSLCERT_SUCCESS, SSLCERT_FAILURE> => {
    return {
        [CALL_API]: {
            endpoint: '/api/v1/ssl_certificates',
            method: 'GET',
            types: [
                SSLCERT_REQUEST,
                SSLCERT_SUCCESS,
                SSLCERT_FAILURE
            ],
            headers: JSONAPI_HEADERS
        }
    }
};