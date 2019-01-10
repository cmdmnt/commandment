import {encodeJSONAPIIndexParameters, RSAAIndexActionRequest, RSAAIndexActionResponse} from "../json-api";
import {ManagedApplication} from "./types";
import {HTTPVerb, RSAA, RSAAction} from "redux-api-middleware";
import {JSONAPI_HEADERS} from "../constants";

export enum ManagedApplicationsActionTypes {
    INDEX_REQUEST = "managed_applications/INDEX_REQUEST",
    INDEX_SUCCESS = "managed_applications/INDEX_SUCCESS",
    INDEX_FAILURE = "managed_applications/INDEX_FAILURE",
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

export type ManagedApplicationsActions = IndexActionResponse;
