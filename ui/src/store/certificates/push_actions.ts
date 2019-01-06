import { RSAA, RSAAction } from 'redux-api-middleware';
import {JSONAPI_HEADERS, FlaskFilters, FlaskFilter} from '../../store/constants'
import {JSONAPIListResponse, JSONAPIDataObject} from "../json-api";
import {Certificate} from "../../store/certificates/types";


export type PUSHCERT_REQUEST = 'certificates/PUSHCERT_REQUEST';
export const PUSHCERT_REQUEST: PUSHCERT_REQUEST = 'certificates/PUSHCERT_REQUEST';
export type PUSHCERT_SUCCESS = 'certificates/PUSHCERT_SUCCESS';
export const PUSHCERT_SUCCESS: PUSHCERT_SUCCESS = 'certificates/PUSHCERT_SUCCESS';
export type PUSHCERT_FAILURE = 'certificates/PUSHCERT_FAILURE';
export const PUSHCERT_FAILURE: PUSHCERT_FAILURE = 'certificates/PUSHCERT_FAILURE';

export interface FetchPushCertificatesActionRequest {
    (): RSAAction<PUSHCERT_REQUEST, PUSHCERT_SUCCESS, PUSHCERT_FAILURE>;
}

export interface FetchPushCertificatesActionResponse {
    type: PUSHCERT_REQUEST | PUSHCERT_SUCCESS | PUSHCERT_FAILURE;
    payload?: JSONAPIListResponse<JSONAPIDataObject<Certificate>>;
}

export const fetchPushCertificates: FetchPushCertificatesActionRequest = (): RSAAction<PUSHCERT_REQUEST, PUSHCERT_SUCCESS, PUSHCERT_FAILURE> => {
    return {
        [RSAA]: {
            endpoint: '/api/v1/push_certificates',
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