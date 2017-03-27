import { CALL_API, RSAA } from 'redux-api-middleware';
import { JSONAPI_HEADERS, CertificatePurpose } from './constants'

export type NEW_REQUEST = 'signing_requests/NEW_REQUEST';
export const NEW_REQUEST: NEW_REQUEST = 'signing_requests/NEW_REQUEST';
export type NEW_SUCCESS = 'signing_requests/NEW_SUCCESS';
export const NEW_SUCCESS: NEW_SUCCESS = 'signing_requests/NEW_SUCCESS';
export type NEW_FAILURE = 'signing_requests/NEW_FAILURE';
export const NEW_FAILURE: NEW_FAILURE = 'signing_requests/NEW_FAILURE';



export const newCertificateSigningRequest = (purpose: CertificatePurpose): RSAA<NEW_REQUEST, NEW_SUCCESS, NEW_FAILURE>  => {
    return {
        [CALL_API]: {
            endpoint: '/api/v1/certificate_signing_requests/new',
            method: 'GET',
            types: [
                NEW_REQUEST,
                NEW_SUCCESS,
                NEW_FAILURE
            ],
            headers: JSONAPI_HEADERS,
            payload: JSON.stringify({ purpose })
        }
    }
};