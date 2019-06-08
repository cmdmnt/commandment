import {HTTPVerb, RSAA, RSAAction} from "redux-api-middleware";
import {encodeJSONAPIChildIndexParameters} from "../../flask-rest-jsonapi";
import {RootState} from "../../reducers";
import {JSONAPI_HEADERS} from "../constants";
import {
    RSAAChildIndexActionRequest,
    RSAAIndexActionResponse,
} from "../json-api";
import {InstalledApplication} from "./types";

export type PROFILES_REQUEST = "devices/PROFILES_REQUEST";
export const PROFILES_REQUEST: PROFILES_REQUEST = "devices/PROFILES_REQUEST";
export type PROFILES_SUCCESS = "devices/PROFILES_SUCCESS";
export const PROFILES_SUCCESS: PROFILES_SUCCESS = "devices/PROFILES_SUCCESS";
export type PROFILES_FAILURE = "devices/PROFILES_FAILURE";
export const PROFILES_FAILURE: PROFILES_FAILURE = "devices/PROFILES_FAILURE";

export type InstalledProfilesActionRequest = RSAAChildIndexActionRequest<PROFILES_REQUEST, PROFILES_SUCCESS, PROFILES_FAILURE>;
export type InstalledProfilesActionResponse = RSAAIndexActionResponse<PROFILES_REQUEST, PROFILES_SUCCESS, PROFILES_FAILURE, InstalledApplication>;

export const profiles = encodeJSONAPIChildIndexParameters((device_id: string, queryParameters: String[])  => {
    const rsaa: RSAAction<PROFILES_REQUEST, PROFILES_SUCCESS, PROFILES_FAILURE> = {
        [RSAA]: {
            endpoint: `/api/v1/devices/${device_id}/installed_profiles?${queryParameters.join("&")}`,
            method: ("GET" as HTTPVerb),
            types: [
                PROFILES_REQUEST,
                PROFILES_SUCCESS,
                PROFILES_FAILURE,
            ],
            headers: (state: RootState) => ({
                ...JSONAPI_HEADERS,
                Authorization: `Bearer ${state.auth.access_token}`,
            }),
        },
    };
    return rsaa;
});
