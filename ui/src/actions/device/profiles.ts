import {JSONAPI_HEADERS} from "../constants";
import {CALL_API} from "redux-api-middleware";
import {encodeJSONAPIChildIndexParameters, RSAAIndexActionRequest, RSAAIndexActionResponse} from "../../constants";
import {InstalledApplication} from "../../models";


export type PROFILES_REQUEST = 'devices/PROFILES_REQUEST';
export const PROFILES_REQUEST: PROFILES_REQUEST = 'devices/PROFILES_REQUEST';
export type PROFILES_SUCCESS = 'devices/PROFILES_SUCCESS';
export const PROFILES_SUCCESS: PROFILES_SUCCESS = 'devices/PROFILES_SUCCESS';
export type PROFILES_FAILURE = 'devices/PROFILES_FAILURE';
export const PROFILES_FAILURE: PROFILES_FAILURE = 'devices/PROFILES_FAILURE';

export type InstalledProfilesActionRequest = RSAAIndexActionRequest<PROFILES_REQUEST, PROFILES_SUCCESS, PROFILES_FAILURE>;
export type InstalledProfilesActionResponse = RSAAIndexActionResponse<PROFILES_REQUEST, PROFILES_SUCCESS, PROFILES_FAILURE, InstalledApplication>;

export const profiles = encodeJSONAPIChildIndexParameters((device_id: number, queryParameters: Array<String>)  => {
    return {
        [CALL_API]: {
            endpoint: `/api/v1/devices/${device_id}/installed_profiles?${queryParameters.join('&')}`,
            method: 'GET',
            types: [
                PROFILES_REQUEST,
                PROFILES_SUCCESS,
                PROFILES_FAILURE
            ],
            headers: JSONAPI_HEADERS
        }
    }
});
