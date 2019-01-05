/// <reference path="../../typings/redux-api-middleware.d.ts" />
import { RSAA, RSAAction } from 'redux-api-middleware';
import {JSONAPI_HEADERS, FlaskFilters, FlaskFilter} from '../../store/constants'
import {JSONAPIListResponse, JSONAPIDataObject} from "../json-api";
import {Certificate} from "./types";


export type SSLCERT_REQUEST = 'certificates/SSLCERT_REQUEST';
export const SSLCERT_REQUEST: SSLCERT_REQUEST = 'certificates/SSLCERT_REQUEST';
export type SSLCERT_SUCCESS = 'certificates/SSLCERT_SUCCESS';
export const SSLCERT_SUCCESS: SSLCERT_SUCCESS = 'certificates/SSLCERT_SUCCESS';
export type SSLCERT_FAILURE = 'certificates/SSLCERT_FAILURE';
export const SSLCERT_FAILURE: SSLCERT_FAILURE = 'certificates/SSLCERT_FAILURE';

export interface FetchSSLCertificatesActionRequest {
    (): RSAAction<SSLCERT_REQUEST, SSLCERT_SUCCESS, SSLCERT_FAILURE>;
}

export interface FetchSSLCertificatesActionResponse {
    type: SSLCERT_REQUEST | SSLCERT_SUCCESS | SSLCERT_FAILURE;
    payload?: JSONAPIListResponse<JSONAPIDataObject<Certificate>>;
}

export const fetchSSLCertificates: FetchSSLCertificatesActionRequest = (): RSAAction<SSLCERT_REQUEST, SSLCERT_SUCCESS, SSLCERT_FAILURE> => {
    return {
        [RSAA]: {
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