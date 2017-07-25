import {JSONAPI_HEADERS} from "../constants";
import {CALL_API, HTTPVerb, RSAA} from "redux-api-middleware";
import {
    encodeJSONAPIChildIndexParameters, RSAAChildIndexActionRequest,
    RSAAIndexActionResponse
} from "../../json-api";
import {InstalledApplication} from "../../models";


export type PROFILES_REQUEST = 'devices/PROFILES_REQUEST';
export const PROFILES_REQUEST: PROFILES_REQUEST = 'devices/PROFILES_REQUEST';
export type PROFILES_SUCCESS = 'devices/PROFILES_SUCCESS';
export const PROFILES_SUCCESS: PROFILES_SUCCESS = 'devices/PROFILES_SUCCESS';
export type PROFILES_FAILURE = 'devices/PROFILES_FAILURE';
export const PROFILES_FAILURE: PROFILES_FAILURE = 'devices/PROFILES_FAILURE';

export type InstalledProfilesActionRequest = RSAAChildIndexActionRequest<PROFILES_REQUEST, PROFILES_SUCCESS, PROFILES_FAILURE>;
export type InstalledProfilesActionResponse = RSAAIndexActionResponse<PROFILES_REQUEST, PROFILES_SUCCESS, PROFILES_FAILURE, InstalledApplication>;

export const profiles = encodeJSONAPIChildIndexParameters((device_id: string, queryParameters: Array<String>)  => {
    const rsaa: RSAA<PROFILES_REQUEST, PROFILES_SUCCESS, PROFILES_FAILURE> = {
        [CALL_API]: {
            endpoint: `/api/v1/devices/${device_id}/installed_profiles?${queryParameters.join('&')}`,
            method: (<HTTPVerb>'GET'),
            types: [
                PROFILES_REQUEST,
                PROFILES_SUCCESS,
                PROFILES_FAILURE
            ],
            headers: JSONAPI_HEADERS
        }
    };
    return rsaa;
});
