import {HTTPVerb, RSAA, RSAAction} from "redux-api-middleware";
import {JSONAPI_HEADERS} from "../constants";
import {
    RSAAChildIndexActionRequest,
    RSAAIndexActionRequest,
    RSAAIndexActionResponse
} from "../json-api";
import {ManagedApplication} from "./types";
import {Command} from "../device/types";
import {DevicesActionTypes} from "../device/actions";
import {encodeJSONAPIChildIndexParameters, encodeJSONAPIIndexParameters} from "../../flask-rest-jsonapi";

export enum ManagedApplicationsActionTypes {
    INDEX_REQUEST = "managed_applications/INDEX_REQUEST",
    INDEX_SUCCESS = "managed_applications/INDEX_SUCCESS",
    INDEX_FAILURE = "managed_applications/INDEX_FAILURE",

    DEVICES_REQUEST = "managed_applications/DEVICES_REQUEST",
    DEVICES_SUCCESS = "managed_applications/DEVICES_SUCCESS",
    DEVICES_FAILURE = "managed_applications/DEVICES_FAILURE",
}

export type IndexActionRequest = RSAAIndexActionRequest<
    ManagedApplicationsActionTypes.INDEX_REQUEST,
    ManagedApplicationsActionTypes.INDEX_SUCCESS,
    ManagedApplicationsActionTypes.INDEX_FAILURE>;

export type IndexActionResponse = RSAAIndexActionResponse<
    ManagedApplicationsActionTypes.INDEX_REQUEST,
    ManagedApplicationsActionTypes.INDEX_SUCCESS,
    ManagedApplicationsActionTypes.INDEX_FAILURE,
    ManagedApplication>;

export const index = encodeJSONAPIIndexParameters((queryParameters: string[]) => {
    return ({
        [RSAA]: {
            endpoint: "/api/v1/managed_applications?" + queryParameters.join("&"),
            headers: JSONAPI_HEADERS,
            method: ("GET" as HTTPVerb),
            types: [
                ManagedApplicationsActionTypes.INDEX_REQUEST,
                ManagedApplicationsActionTypes.INDEX_SUCCESS,
                ManagedApplicationsActionTypes.INDEX_FAILURE,
            ],
        },
    } as RSAAction<ManagedApplicationsActionTypes.INDEX_REQUEST,
        ManagedApplicationsActionTypes.INDEX_SUCCESS,
        ManagedApplicationsActionTypes.INDEX_FAILURE>);
});

export type DevicesActionRequest = RSAAChildIndexActionRequest<
    ManagedApplicationsActionTypes.DEVICES_REQUEST,
    ManagedApplicationsActionTypes.DEVICES_SUCCESS,
    ManagedApplicationsActionTypes.DEVICES_FAILURE>;
export type DevicesActionResponse = RSAAIndexActionResponse<
    ManagedApplicationsActionTypes.DEVICES_REQUEST,
    ManagedApplicationsActionTypes.DEVICES_SUCCESS,
    ManagedApplicationsActionTypes.DEVICES_FAILURE,
    Command>;

export const devices = encodeJSONAPIChildIndexParameters((managedAppId: string, queryParameters: string[])  => {
    return ({
        [RSAA]: {
            endpoint: `/api/v1/managed_applications/${managedAppId}/devices?${queryParameters.join("&")}`,
            headers: JSONAPI_HEADERS,
            method: "GET",
            types: [
                ManagedApplicationsActionTypes.DEVICES_REQUEST,
                ManagedApplicationsActionTypes.DEVICES_SUCCESS,
                ManagedApplicationsActionTypes.DEVICES_FAILURE,
            ],
        },
    } as RSAAction<
        ManagedApplicationsActionTypes.DEVICES_REQUEST,
        ManagedApplicationsActionTypes.DEVICES_SUCCESS,
        ManagedApplicationsActionTypes.DEVICES_FAILURE>);
});

export type ManagedApplicationsActions = IndexActionResponse;
