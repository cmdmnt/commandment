import {JSONAPI_HEADERS} from "../constants";
import {CALL_API} from "redux-api-middleware";
import {
    encodeJSONAPIChildIndexParameters, RSAAChildIndexActionRequest,
    RSAAIndexActionResponse
} from "../../json-api";
import {InstalledCertificate} from "../../models";


export type CERTIFICATES_REQUEST = 'devices/CERTIFICATES_REQUEST';
export const CERTIFICATES_REQUEST: CERTIFICATES_REQUEST = 'devices/CERTIFICATES_REQUEST';
export type CERTIFICATES_SUCCESS = 'devices/CERTIFICATES_SUCCESS';
export const CERTIFICATES_SUCCESS: CERTIFICATES_SUCCESS = 'devices/CERTIFICATES_SUCCESS';
export type CERTIFICATES_FAILURE = 'devices/CERTIFICATES_FAILURE';
export const CERTIFICATES_FAILURE: CERTIFICATES_FAILURE = 'devices/CERTIFICATES_FAILURE';

export type CertificatesActionRequest = RSAAChildIndexActionRequest<CERTIFICATES_REQUEST, CERTIFICATES_SUCCESS, CERTIFICATES_FAILURE>;
export type CertificatesActionResponse = RSAAIndexActionResponse<CERTIFICATES_REQUEST, CERTIFICATES_SUCCESS, CERTIFICATES_FAILURE, InstalledCertificate>;

export const certificates = encodeJSONAPIChildIndexParameters((device_id: number, queryParameters: Array<String>)  => {
    return {
        [CALL_API]: {
            endpoint: `/api/v1/devices/${device_id}/installed_certificates?${queryParameters.join('&')}`,
            method: 'GET',
            types: [
                CERTIFICATES_REQUEST,
                CERTIFICATES_SUCCESS,
                CERTIFICATES_FAILURE
            ],
            headers: JSONAPI_HEADERS
        }
    }
});