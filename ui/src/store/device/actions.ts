/// <reference path="../../typings/redux-api-middleware.d.ts" />
import {Dispatch} from "react-redux";
import {Action} from "redux";
import {HTTPVerb, RSAA, RSAAction} from "redux-api-middleware";
import {ThunkAction} from "redux-thunk";
import {
    encodeJSONAPIChildIndexParameters, encodeJSONAPIIndexParameters, JSONAPIRelationship, JSONAPIRelationships,
    RSAAChildIndexActionRequest,
    RSAAIndexActionRequest,
    RSAAIndexActionResponse, RSAAPatchActionRequest, RSAAReadActionRequest, RSAAReadActionResponse,
} from "../../json-api";
import {JSONAPIDetailResponse, JSONAPIErrorResponse} from "../../json-api";
import {RootState} from "../../reducers/index";
import {FlaskFilter, FlaskFilters, JSON_HEADERS, JSONAPI_HEADERS} from "../constants"
import {Tag} from "../tags/types";
import {Command, Device, DeviceRelationship} from "./types";

export enum DevicesActionTypes {
    INDEX_REQUEST = "devices/INDEX_REQUEST",
    INDEX_SUCCESS = "devices/INDEX_SUCCESS",
    INDEX_FAILURE = "devices/INDEX_FAILURE",
    READ_REQUEST = "devices/READ_REQUEST",
    READ_SUCCESS = "devices/READ_SUCCESS",
    READ_FAILURE = "devices/READ_FAILURE",
    PUSH_REQUEST = "devices/PUSH_REQUEST",
    PUSH_SUCCESS = "devices/PUSH_SUCCESS",
    PUSH_FAILURE = "devices/PUSH_FAILURE",
    RESTART_REQUEST = "devices/RESTART_REQUEST",
    RESTART_SUCCESS = "devices/RESTART_SUCCESS",
    RESTART_FAILURE = "devices/RESTART_FAILURE",
    SHUTDOWN_REQUEST = "devices/SHUTDOWN_REQUEST",
    SHUTDOWN_SUCCESS = "devices/SHUTDOWN_SUCCESS",
    SHUTDOWN_FAILURE = "devices/SHUTDOWN_FAILURE",
    INVENTORY_REQUEST = "devices/INVENTORY_REQUEST",
    INVENTORY_SUCCESS = "devices/INVENTORY_SUCCESS",
    INVENTORY_FAILURE = "devices/INVENTORY_FAILURE",
    COMMANDS_REQUEST = "devices/COMMANDS_REQUEST",
    COMMANDS_SUCCESS = "devices/COMMANDS_SUCCESS",
    COMMANDS_FAILURE = "devices/COMMANDS_FAILURE",
}

export type IndexActionRequest = RSAAIndexActionRequest<DevicesActionTypes.INDEX_REQUEST, DevicesActionTypes.INDEX_SUCCESS, DevicesActionTypes.INDEX_FAILURE>;
export type IndexActionResponse = RSAAIndexActionResponse<DevicesActionTypes.INDEX_REQUEST, DevicesActionTypes.INDEX_SUCCESS, DevicesActionTypes.INDEX_FAILURE, Device>;

export const index = encodeJSONAPIIndexParameters((queryParameters: String[]) => {
    return ({
        [RSAA]: {
            endpoint: "/api/v1/devices?" + queryParameters.join("&"),
            method: ("GET" as HTTPVerb),
            types: [
                DevicesActionTypes.INDEX_REQUEST,
                DevicesActionTypes.INDEX_SUCCESS,
                DevicesActionTypes.INDEX_FAILURE,
            ],
            headers: JSONAPI_HEADERS,
        },
    } as RSAAction<DevicesActionTypes.INDEX_REQUEST, DevicesActionTypes.INDEX_SUCCESS, DevicesActionTypes.INDEX_FAILURE>);
});

export const fetchDevicesIfRequired = (
        size: number = 10,
        pageNumber: number = 1,
        sort?: string[],
        filters?: FlaskFilters,
    ) => (dispatch: Dispatch<RootState>, getState: () => RootState): ThunkAction<void, RootState, {}> => {

    const { devices } = getState();
    if (devices.lastReceived) {
        const now = new Date();
        const seconds = 10;
        if ((now.getTime() - devices.lastReceived.getTime()) / 1000 < seconds) {
            console.log("cache hit");
            return;
        }
    }

    dispatch(index(size, pageNumber, sort, filters));
};

export type ReadActionRequest = RSAAReadActionRequest<DevicesActionTypes.READ_REQUEST, DevicesActionTypes.READ_SUCCESS, DevicesActionTypes.READ_FAILURE>;
export type ReadActionResponse = RSAAReadActionResponse<DevicesActionTypes.READ_REQUEST, DevicesActionTypes.READ_SUCCESS, DevicesActionTypes.READ_FAILURE, JSONAPIDetailResponse<Device, undefined>>;

export const read: ReadActionRequest = (id: string, include?: string[]) => {

    let inclusions = "";
    if (include && include.length) {
        inclusions = "include=" + include.join(",")
    }

    return {
        [RSAA]: {
            endpoint: `/api/v1/devices/${id}?${inclusions}`,
            headers: JSONAPI_HEADERS,
            method: "GET",
            types: [
                DevicesActionTypes.READ_REQUEST,
                DevicesActionTypes.READ_SUCCESS,
                DevicesActionTypes.READ_FAILURE,
            ],
        },
    }
};

export const READ_CACHE_HIT = "devices/READ_CACHE_HIT";
export type READ_CACHE_HIT = typeof READ_CACHE_HIT;

export type CacheFetchActionRequest = (id: string, include?: string[]) => ThunkAction<void, RootState, any>;

export const fetchDeviceIfRequired = (
    id: string, include?: string[],
) => (
    dispatch: Dispatch<RootState>,
    getState: () => RootState,
) => {
    const { devices } = getState();

    // if (devices.lastReceived) {
    //     const now = new Date();
    //     const seconds = 10;
    //     if ((now.getTime() - devices.lastReceived.getTime()) / 1000 < seconds) {
    //         if (devices.byId.hasOwnProperty(id)) {
    //             dispatch({type: READ_CACHE_HIT, id});
    //             const payload = {
    //                 type: READ_SUCCESS,
    //                 payload: {
    //                     data: devices.byId[id]
    //                 }
    //             };
    //             dispatch(payload);
    //             return;
    //         }
    //     }
    // }

    dispatch(read(id, include));
};

export type PushActionRequest = (id: string) =>
    RSAAction<DevicesActionTypes.PUSH_REQUEST, DevicesActionTypes.PUSH_SUCCESS, DevicesActionTypes.PUSH_FAILURE>;

export interface PushActionResponse {
    type: DevicesActionTypes.PUSH_REQUEST | DevicesActionTypes.PUSH_SUCCESS | DevicesActionTypes.PUSH_FAILURE;
    payload?: JSONAPIDetailResponse<any, undefined> | JSONAPIErrorResponse;
}

export const push: PushActionRequest = (id: string) => {
    return {
        [RSAA]: {
            endpoint: `/api/v1/devices/${id}/push`,
            headers: JSON_HEADERS,
            method: "POST",
            types: [
                DevicesActionTypes.PUSH_REQUEST,
                DevicesActionTypes.PUSH_SUCCESS,
                DevicesActionTypes.PUSH_FAILURE,
            ],
        },
    }
};

export type RestartActionRequest = (id: string) =>
    RSAAction<DevicesActionTypes.RESTART_REQUEST, DevicesActionTypes.RESTART_SUCCESS, DevicesActionTypes.RESTART_FAILURE>;

export interface RestartActionResponse {
    type: DevicesActionTypes.RESTART_REQUEST | DevicesActionTypes.RESTART_SUCCESS | DevicesActionTypes.RESTART_FAILURE;
    payload?: JSONAPIDetailResponse<any, undefined> | JSONAPIErrorResponse;
}

export const restart: RestartActionRequest = (id: string) => {
    return {
        [RSAA]: {
            endpoint: `/api/v1/devices/${id}/restart`,
            headers: JSON_HEADERS,
            method: "POST",
            types: [
                DevicesActionTypes.RESTART_REQUEST,
                DevicesActionTypes.RESTART_SUCCESS,
                DevicesActionTypes.RESTART_FAILURE,
            ],
        },
    }
};

export type ShutdownActionRequest = (id: string) =>
    RSAAction<DevicesActionTypes.SHUTDOWN_REQUEST, DevicesActionTypes.SHUTDOWN_SUCCESS, DevicesActionTypes.SHUTDOWN_FAILURE>;

export interface ShutdownActionResponse {
    type: DevicesActionTypes.SHUTDOWN_REQUEST | DevicesActionTypes.SHUTDOWN_SUCCESS | DevicesActionTypes.SHUTDOWN_FAILURE;
    payload?: JSONAPIDetailResponse<any, undefined> | JSONAPIErrorResponse;
}

export const shutdown: ShutdownActionRequest = (id: string) => {
    return {
        [RSAA]: {
            endpoint: `/api/v1/devices/${id}/shutdown`,
            headers: JSON_HEADERS,
            method: "POST",
            types: [
                DevicesActionTypes.SHUTDOWN_REQUEST,
                DevicesActionTypes.SHUTDOWN_SUCCESS,
                DevicesActionTypes.SHUTDOWN_FAILURE,
            ],
        },
    }
};

export type InventoryActionRequest = (id: string) =>
    RSAAction<DevicesActionTypes.INVENTORY_REQUEST, DevicesActionTypes.INVENTORY_SUCCESS, DevicesActionTypes.INVENTORY_FAILURE>;

export interface InventoryActionResponse {
    type: DevicesActionTypes.INVENTORY_REQUEST | DevicesActionTypes.INVENTORY_SUCCESS | DevicesActionTypes.INVENTORY_FAILURE;
    payload?: JSONAPIDetailResponse<any, undefined> | JSONAPIErrorResponse;
}

export const inventory: InventoryActionRequest = (id: string) => {
    return {
        [RSAA]: {
            endpoint: `/api/v1/devices/inventory/${id}`,
            method: "GET",
            types: [
                DevicesActionTypes.INVENTORY_REQUEST,
                DevicesActionTypes.INVENTORY_SUCCESS,
                DevicesActionTypes.INVENTORY_FAILURE,
            ],
            headers: JSON_HEADERS,
        },
    }
};

export type TEST_REQUEST = "devices/TEST_REQUEST";
export const TEST_REQUEST: TEST_REQUEST = "devices/TEST_REQUEST";
export type TEST_SUCCESS = "devices/TEST_SUCCESS";
export const TEST_SUCCESS: TEST_SUCCESS = "devices/TEST_SUCCESS";
export type TEST_FAILURE = "devices/TEST_FAILURE";
export const TEST_FAILURE: TEST_FAILURE = "devices/TEST_FAILURE";

type TestActionRequest = (id: string) => RSAAction<TEST_REQUEST, TEST_SUCCESS, TEST_FAILURE>;

export interface TestActionResponse {
    type: TEST_REQUEST | TEST_SUCCESS | TEST_FAILURE;
    payload?: JSONAPIDetailResponse<any, undefined> | JSONAPIErrorResponse;
}

export const test: TestActionRequest = (id: string) => {
    return {
        [RSAA]: {
            endpoint: `/api/v1/devices/test/${id}`,
            method: "POST",
            types: [
                TEST_REQUEST,
                TEST_SUCCESS,
                TEST_FAILURE,
            ],
            headers: JSON_HEADERS,
        },
    }
};

export type CommandsActionRequest = RSAAChildIndexActionRequest<DevicesActionTypes.COMMANDS_REQUEST, DevicesActionTypes.COMMANDS_SUCCESS, DevicesActionTypes.COMMANDS_FAILURE>;
export type CommandsActionResponse = RSAAIndexActionResponse<DevicesActionTypes.COMMANDS_REQUEST, DevicesActionTypes.COMMANDS_SUCCESS, DevicesActionTypes.COMMANDS_FAILURE, Command>;

export const commands = encodeJSONAPIChildIndexParameters((device_id: string, queryParameters: String[])  => {
    return ({
        [RSAA]: {
            endpoint: `/api/v1/devices/${device_id}/commands?${queryParameters.join("&")}`,
            method: "GET",
            types: [
                DevicesActionTypes.COMMANDS_REQUEST,
                DevicesActionTypes.COMMANDS_SUCCESS,
                DevicesActionTypes.COMMANDS_FAILURE,
            ],
            headers: JSONAPI_HEADERS,
        },
    } as RSAAction<DevicesActionTypes.COMMANDS_REQUEST, DevicesActionTypes.COMMANDS_SUCCESS, DevicesActionTypes.COMMANDS_FAILURE>);
});

export const PATCH_REQUEST = "devices/PATCH_REQUEST";
export type PATCH_REQUEST = typeof PATCH_REQUEST;
export const PATCH_SUCCESS = "devices/PATCH_SUCCESS";
export type PATCH_SUCCESS = typeof PATCH_SUCCESS;
export const PATCH_FAILURE = "devices/PATCH_FAILURE";
export type PATCH_FAILURE = typeof PATCH_FAILURE;

export type PatchActionRequest = RSAAPatchActionRequest<PATCH_REQUEST, PATCH_SUCCESS, PATCH_FAILURE, Device>;
export type PatchActionResponse = RSAAReadActionResponse<PATCH_REQUEST, PATCH_SUCCESS, PATCH_FAILURE, JSONAPIDetailResponse<Device, Tag>>;

export const patch: PatchActionRequest = (device_id: string, values: Device) => {

    return {
        [RSAA]: {
            endpoint: `/api/v1/devices/${device_id}`,
            method: "PATCH",
            types: [
                PATCH_REQUEST,
                PATCH_SUCCESS,
                PATCH_FAILURE,
            ],
            headers: JSONAPI_HEADERS,
            body: JSON.stringify({
                data: {
                    type: "devices",
                    attributes: values,
                },
            }),
        },
    }
};

export const RPOST_REQUEST = "devices/RPOST_REQUEST";
export type RPOST_REQUEST = typeof RPOST_REQUEST;
export const RPOST_SUCCESS = "devices/RPOST_SUCCESS";
export type RPOST_SUCCESS = typeof RPOST_SUCCESS;
export const RPOST_FAILURE = "devices/RPOST_FAILURE";
export type RPOST_FAILURE = typeof RPOST_FAILURE;

type PostRelationshipActionRequest = (parent_id: string, relationship: DeviceRelationship, data: JSONAPIRelationship[]) => RSAAction<RPOST_REQUEST, RPOST_SUCCESS, RPOST_FAILURE>;
export type PostRelationshipActionResponse = RSAAReadActionResponse<RPOST_REQUEST, RPOST_SUCCESS, RPOST_FAILURE, JSONAPIDetailResponse<Device, undefined>>;

export const postRelationship: PostRelationshipActionRequest = (id: string, relationship: DeviceRelationship, data: JSONAPIRelationship[]) => {
    return {
        [RSAA]: {
            endpoint: `/api/v1/devices/${id}/relationships/${relationship}`,
            method: "POST",
            types: [
                RPOST_REQUEST,
                RPOST_SUCCESS,
                RPOST_FAILURE,
            ],
            headers: JSONAPI_HEADERS,
            body: JSON.stringify({ data }),
        },
    }
};

export const RCPOST_REQUEST = "devices/RCPOST_REQUEST";
export type RCPOST_REQUEST = typeof RCPOST_REQUEST;
export const RCPOST_SUCCESS = "devices/RCPOST_SUCCESS";
export type RCPOST_SUCCESS = typeof RCPOST_SUCCESS;
export const RCPOST_FAILURE = "devices/RCPOST_FAILURE";
export type RCPOST_FAILURE = typeof RCPOST_FAILURE;

type PostRelatedActionRequest = <TRelated>(parent_id: string, relationship: DeviceRelationship, data: TRelated) => RSAAction<RCPOST_REQUEST, RCPOST_SUCCESS, RCPOST_FAILURE>;
export type PostRelatedActionResponse = RSAAReadActionResponse<RCPOST_REQUEST, RCPOST_SUCCESS, RCPOST_FAILURE, JSONAPIDetailResponse<any, undefined>>;

export const postRelated: PostRelatedActionRequest = <TRelated>(parent_id: string, relationship: DeviceRelationship, data: TRelated): RSAAction<RCPOST_REQUEST, RCPOST_SUCCESS, RCPOST_FAILURE> => {
    return {
        [RSAA]: {
            endpoint: `/api/v1/devices/${parent_id}/${relationship}`,
            method: "POST",
            types: [
                RCPOST_REQUEST,
                RCPOST_SUCCESS,
                RCPOST_FAILURE,
            ],
            headers: JSONAPI_HEADERS,
            body: JSON.stringify({ data: {
                type: relationship,
                attributes: data,
                relationships: {
                    devices: {
                        data: [
                            {
                                type: "devices",
                                id: parent_id,
                            },
                        ],
                    },
                },
            } }),
        },
    }
};

export const RPATCH_REQUEST = "devices/RPATCH_REQUEST";
export type RPATCH_REQUEST = typeof RPATCH_REQUEST;
export const RPATCH_SUCCESS = "devices/RPATCH_SUCCESS";
export type RPATCH_SUCCESS = typeof RPATCH_SUCCESS;
export const RPATCH_FAILURE = "devices/RPATCH_FAILURE";
export type RPATCH_FAILURE = typeof RPATCH_FAILURE;

type PatchRelationshipActionRequest = (parent_id: string, relationship: DeviceRelationship, data: JSONAPIRelationship[]) => RSAAction<RPATCH_REQUEST, RPATCH_SUCCESS, RPATCH_FAILURE>;
export type PatchRelationshipActionResponse = RSAAReadActionResponse<RPATCH_REQUEST, RPATCH_SUCCESS, RPATCH_FAILURE, JSONAPIDetailResponse<Device, undefined>>;

export const patchRelationship: PatchRelationshipActionRequest = (id: string, relationship: DeviceRelationship, data: JSONAPIRelationship[]) => {
    return {
        [RSAA]: {
            endpoint: `/api/v1/devices/${id}/relationships/${relationship}`,
            method: "PATCH",
            types: [
                RPATCH_REQUEST,
                RPATCH_SUCCESS,
                RPATCH_FAILURE,
            ],
            headers: JSONAPI_HEADERS,
            body: JSON.stringify({ data }),
        },
    }
};
