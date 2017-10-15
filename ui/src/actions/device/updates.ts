import {JSONAPI_HEADERS} from "../constants";
import {RSAA, HTTPVerb, RSAAction} from "redux-api-middleware";
import {
    encodeJSONAPIChildIndexParameters, RSAAChildIndexActionRequest,
    RSAAIndexActionResponse
} from "../../json-api";
import {AvailableOSUpdate} from "../../models";


export const UPDATES_REQUEST = 'devices/UPDATES_REQUEST';
export type UPDATES_REQUEST = typeof UPDATES_REQUEST;
export const UPDATES_SUCCESS = 'devices/UPDATES_SUCCESS';
export type UPDATES_SUCCESS = typeof UPDATES_SUCCESS;
export const UPDATES_FAILURE = 'devices/UPDATES_FAILURE';
export type UPDATES_FAILURE = typeof UPDATES_FAILURE;

export type AvailableOSUpdatesActionRequest = RSAAChildIndexActionRequest<UPDATES_REQUEST, UPDATES_SUCCESS, UPDATES_FAILURE>;
export type AvailableOSUpdatesActionResponse = RSAAIndexActionResponse<UPDATES_REQUEST, UPDATES_SUCCESS, UPDATES_FAILURE, AvailableOSUpdate>;

export const updates = encodeJSONAPIChildIndexParameters((device_id: string, queryParameters: Array<String>)  => {
    return (<RSAAction<UPDATES_REQUEST, UPDATES_SUCCESS, UPDATES_FAILURE>>{
        [RSAA]: {
            endpoint: `/api/v1/devices/${device_id}/available_os_updates?${queryParameters.join('&')}`,
            method: (<HTTPVerb>'GET'),
            types: [
                UPDATES_REQUEST, UPDATES_SUCCESS, UPDATES_FAILURE
            ],
            headers: JSONAPI_HEADERS
        }
    });
});
