/// <reference path="../../typings/redux-api-middleware.d.ts" />
import { RSAA, RSAAction } from 'redux-api-middleware';
import {JSONAPI_HEADERS, FlaskFilters, FlaskFilter} from '../../store/constants'
import {JSONAPIListResponse, JSONAPIDataObject} from "../../json-api";
import {Certificate} from "../../store/certificates/types";


export type CACERT_REQUEST = 'certificates/CACERT_REQUEST';
export const CACERT_REQUEST: CACERT_REQUEST = 'certificates/CACERT_REQUEST';
export type CACERT_SUCCESS = 'certificates/CACERT_SUCCESS';
export const CACERT_SUCCESS: CACERT_SUCCESS = 'certificates/CACERT_SUCCESS';
export type CACERT_FAILURE = 'certificates/CACERT_FAILURE';
export const CACERT_FAILURE: CACERT_FAILURE = 'certificates/CACERT_FAILURE';

export interface FetchCACertificatesActionRequest {
    (): RSAAction<CACERT_REQUEST, CACERT_SUCCESS, CACERT_FAILURE>;
}

export interface FetchCACertificatesActionResponse {
    type: CACERT_REQUEST | CACERT_SUCCESS | CACERT_FAILURE;
    payload?: JSONAPIListResponse<JSONAPIDataObject<Certificate>>;
}

export const fetchCACertificates: FetchCACertificatesActionRequest = (): RSAAction<CACERT_REQUEST, CACERT_SUCCESS, CACERT_FAILURE> => {
    return {
        [RSAA]: {
            endpoint: '/api/v1/ca_certificates',
            method: 'GET',
            types: [
                CACERT_REQUEST,
                CACERT_SUCCESS,
                CACERT_FAILURE
            ],
            headers: JSONAPI_HEADERS
        }
    }
};