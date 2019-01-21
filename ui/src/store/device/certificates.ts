import {JSONAPI_HEADERS} from "../constants";
import {RSAA, HTTPVerb, RSAAction} from "redux-api-middleware";
import {
    RSAAChildIndexActionRequest,
    RSAAIndexActionResponse
} from "../json-api";
import {InstalledCertificate} from "./types";
import {encodeJSONAPIChildIndexParameters} from "../../flask-rest-jsonapi";


export type CERTIFICATES_REQUEST = 'devices/CERTIFICATES_REQUEST';
export const CERTIFICATES_REQUEST: CERTIFICATES_REQUEST = 'devices/CERTIFICATES_REQUEST';
export type CERTIFICATES_SUCCESS = 'devices/CERTIFICATES_SUCCESS';
export const CERTIFICATES_SUCCESS: CERTIFICATES_SUCCESS = 'devices/CERTIFICATES_SUCCESS';
export type CERTIFICATES_FAILURE = 'devices/CERTIFICATES_FAILURE';
export const CERTIFICATES_FAILURE: CERTIFICATES_FAILURE = 'devices/CERTIFICATES_FAILURE';

export type CertificatesActionRequest = RSAAChildIndexActionRequest<CERTIFICATES_REQUEST, CERTIFICATES_SUCCESS, CERTIFICATES_FAILURE>;
export type CertificatesActionResponse = RSAAIndexActionResponse<CERTIFICATES_REQUEST, CERTIFICATES_SUCCESS, CERTIFICATES_FAILURE, InstalledCertificate>;

export const certificates = encodeJSONAPIChildIndexParameters((device_id: string, queryParameters: Array<String>)  => {
    return (<RSAAction<CERTIFICATES_REQUEST, CERTIFICATES_SUCCESS, CERTIFICATES_FAILURE>>{
        [RSAA]: {
            endpoint: `/api/v1/devices/${device_id}/installed_certificates?${queryParameters.join('&')}`,
            method: (<HTTPVerb>'GET'),
            types: [
                CERTIFICATES_REQUEST,
                CERTIFICATES_SUCCESS,
                CERTIFICATES_FAILURE
            ],
            headers: JSONAPI_HEADERS
        }
    });
});
