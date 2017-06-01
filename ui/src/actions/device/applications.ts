import {JSONAPI_HEADERS} from "../constants";
import {CALL_API} from "redux-api-middleware";
import {encodeJSONAPIChildIndexParameters, RSAAIndexActionRequest, RSAAIndexActionResponse} from "../../json-api";
import {InstalledApplication} from "../../models";


export type APPLICATIONS_REQUEST = 'devices/APPLICATIONS_REQUEST';
export const APPLICATIONS_REQUEST: APPLICATIONS_REQUEST = 'devices/APPLICATIONS_REQUEST';
export type APPLICATIONS_SUCCESS = 'devices/APPLICATIONS_SUCCESS';
export const APPLICATIONS_SUCCESS: APPLICATIONS_SUCCESS = 'devices/APPLICATIONS_SUCCESS';
export type APPLICATIONS_FAILURE = 'devices/APPLICATIONS_FAILURE';
export const APPLICATIONS_FAILURE: APPLICATIONS_FAILURE = 'devices/APPLICATIONS_FAILURE';

export type InstalledApplicationsActionRequest = RSAAIndexActionRequest<APPLICATIONS_REQUEST, APPLICATIONS_SUCCESS, APPLICATIONS_FAILURE>;
export type InstalledApplicationsActionResponse = RSAAIndexActionResponse<APPLICATIONS_REQUEST, APPLICATIONS_SUCCESS, APPLICATIONS_FAILURE, InstalledApplication>;

export const applications = encodeJSONAPIChildIndexParameters((device_id: number, queryParameters: Array<String>)  => {
    return {
        [CALL_API]: {
            endpoint: `/api/v1/devices/${device_id}/installed_applications?${queryParameters.join('&')}`,
            method: 'GET',
            types: [
                APPLICATIONS_REQUEST,
                APPLICATIONS_SUCCESS,
                APPLICATIONS_FAILURE
            ],
            headers: JSONAPI_HEADERS
        }
    }
});
