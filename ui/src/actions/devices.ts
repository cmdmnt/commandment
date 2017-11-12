/// <reference path="../typings/redux-api-middleware.d.ts" />
import {Dispatch} from "react-redux";
import {Action} from "redux";
import {HTTPVerb, RSAA, RSAAction} from "redux-api-middleware";
import {ThunkAction} from "redux-thunk";
import {
    encodeJSONAPIChildIndexParameters, encodeJSONAPIIndexParameters, JSONAPIRelationship, JSONAPIRelationships,
    RSAAChildIndexActionRequest,
    RSAAIndexActionRequest,
    RSAAIndexActionResponse, RSAAPatchActionRequest, RSAAReadActionRequest, RSAAReadActionResponse,
} from "../json-api";
import {JSONAPIDetailResponse, JSONAPIErrorResponse} from "../json-api";
import {Command, Device, DeviceRelationship, Tag} from "../models";
import {IRootState} from "../reducers/index";
import {FlaskFilter, FlaskFilters, JSON_HEADERS, JSONAPI_HEADERS} from "./constants";

export type INDEX_REQUEST = "devices/INDEX_REQUEST";
export const INDEX_REQUEST: INDEX_REQUEST = "devices/INDEX_REQUEST";
export type INDEX_SUCCESS = "devices/INDEX_SUCCESS";
export const INDEX_SUCCESS: INDEX_SUCCESS = "devices/INDEX_SUCCESS";
export type INDEX_FAILURE = "devices/INDEX_FAILURE";
export const INDEX_FAILURE: INDEX_FAILURE = "devices/INDEX_FAILURE";

export type IndexActionRequest = RSAAIndexActionRequest<INDEX_REQUEST, INDEX_SUCCESS, INDEX_FAILURE>;
export type IndexActionResponse = RSAAIndexActionResponse<INDEX_REQUEST, INDEX_SUCCESS, INDEX_FAILURE, Device>;

export const index = encodeJSONAPIIndexParameters((queryParameters: string[]) => {
    return ({
        [RSAA]: {
            endpoint: "/api/v1/devices?" + encodeURI(queryParameters.join("&")),
            headers: JSONAPI_HEADERS,
            method: ("GET" as HTTPVerb),
            types: [
                INDEX_REQUEST,
                INDEX_SUCCESS,
                INDEX_FAILURE,
            ],
        },
    } as RSAAction<INDEX_REQUEST, INDEX_SUCCESS, INDEX_FAILURE>);
});

export const fetchDevicesIfRequired = (
        size: number = 10,
        pageNumber: number = 1,
        sort?: string[],
        filters?: FlaskFilters,
    ) => (dispatch: Dispatch<IRootState>, getState: () => IRootState): ThunkAction<void, IRootState, {}> => {

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

export type READ_REQUEST = "devices/READ_REQUEST";
export const READ_REQUEST: READ_REQUEST = "devices/READ_REQUEST";
export type READ_SUCCESS = "devices/READ_SUCCESS";
export const READ_SUCCESS: READ_SUCCESS = "devices/READ_SUCCESS";
export type READ_FAILURE = "devices/READ_FAILURE";
export const READ_FAILURE: READ_FAILURE = "devices/READ_FAILURE";

export type ReadActionRequest = RSAAReadActionRequest<READ_REQUEST, READ_SUCCESS, READ_FAILURE>;
export type ReadActionResponse = RSAAReadActionResponse<READ_REQUEST, READ_SUCCESS, READ_FAILURE, JSONAPIDetailResponse<Device, undefined>>;

export const read: ReadActionRequest = (id: string, include?: string[]) => {

    let inclusions = "";
    if (include && include.length) {
        inclusions = "include=" + include.join(",");
    }

    return {
        [RSAA]: {
            endpoint: `/api/v1/devices/${id}?${inclusions}`,
            headers: JSONAPI_HEADERS,
            method: "GET",
            types: [
                READ_REQUEST,
                READ_SUCCESS,
                READ_FAILURE,
            ],
        },
    };
};

export const READ_CACHE_HIT = "devices/READ_CACHE_HIT";
export type READ_CACHE_HIT = typeof READ_CACHE_HIT;

export type CacheFetchActionRequest = (id: string, include?: string[]) => ThunkAction<void, IRootState, any>;

export const fetchDeviceIfRequired = (
    id: string, include?: string[],
) => (
    dispatch: Dispatch<IRootState>,
    getState: () => IRootState,
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

export type PUSH_REQUEST = "devices/PUSH_REQUEST";
export const PUSH_REQUEST: PUSH_REQUEST = "devices/PUSH_REQUEST";
export type PUSH_SUCCESS = "devices/PUSH_SUCCESS";
export const PUSH_SUCCESS: PUSH_SUCCESS = "devices/PUSH_SUCCESS";
export type PUSH_FAILURE = "devices/PUSH_FAILURE";
export const PUSH_FAILURE: PUSH_FAILURE = "devices/PUSH_FAILURE";

type PushActionRequest = (id: string) => RSAAction<PUSH_REQUEST, PUSH_SUCCESS, PUSH_FAILURE>;

export interface PushActionResponse {
    type: PUSH_REQUEST | PUSH_SUCCESS | PUSH_FAILURE;
    payload?: JSONAPIDetailResponse<any, undefined> | JSONAPIErrorResponse;
}

export const push: PushActionRequest = (id: string) => {
    return {
        [RSAA]: {
            endpoint: `/api/v1/devices/${id}/push`,
            method: "POST",
            types: [
                PUSH_REQUEST,
                PUSH_SUCCESS,
                PUSH_FAILURE,
            ],
            headers: JSON_HEADERS,
        },
    };
};

export type INVENTORY_REQUEST = "devices/INVENTORY_REQUEST";
export const INVENTORY_REQUEST: INVENTORY_REQUEST = "devices/INVENTORY_REQUEST";
export type INVENTORY_SUCCESS = "devices/INVENTORY_SUCCESS";
export const INVENTORY_SUCCESS: INVENTORY_SUCCESS = "devices/INVENTORY_SUCCESS";
export type INVENTORY_FAILURE = "devices/INVENTORY_FAILURE";
export const INVENTORY_FAILURE: INVENTORY_FAILURE = "devices/INVENTORY_FAILURE";

type InventoryActionRequest = (id: string) => RSAAction<INVENTORY_REQUEST, INVENTORY_SUCCESS, INVENTORY_FAILURE>;

export interface InventoryActionResponse {
    type: INVENTORY_REQUEST | INVENTORY_SUCCESS | INVENTORY_FAILURE;
    payload?: JSONAPIDetailResponse<any, undefined> | JSONAPIErrorResponse;
}

export const inventory: InventoryActionRequest = (id: string) => {
    return {
        [RSAA]: {
            endpoint: `/api/v1/devices/inventory/${id}`,
            headers: JSON_HEADERS,
            method: "GET",
            types: [
                INVENTORY_REQUEST,
                INVENTORY_SUCCESS,
                INVENTORY_FAILURE,
            ],
        },
    };
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
            headers: JSON_HEADERS,
            method: "POST",
            types: [
                TEST_REQUEST,
                TEST_SUCCESS,
                TEST_FAILURE,
            ],
        },
    };
};

export type COMMANDS_REQUEST = "devices/COMMANDS_REQUEST";
export const COMMANDS_REQUEST: COMMANDS_REQUEST = "devices/COMMANDS_REQUEST";
export type COMMANDS_SUCCESS = "devices/COMMANDS_SUCCESS";
export const COMMANDS_SUCCESS: COMMANDS_SUCCESS = "devices/COMMANDS_SUCCESS";
export type COMMANDS_FAILURE = "devices/COMMANDS_FAILURE";
export const COMMANDS_FAILURE: COMMANDS_FAILURE = "devices/COMMANDS_FAILURE";

export type CommandsActionRequest = RSAAChildIndexActionRequest<COMMANDS_REQUEST, COMMANDS_SUCCESS, COMMANDS_FAILURE>;
export type CommandsActionResponse = RSAAIndexActionResponse<COMMANDS_REQUEST, COMMANDS_SUCCESS, COMMANDS_FAILURE, Command>;

export const commands = encodeJSONAPIChildIndexParameters((device_id: string, queryParameters: String[])  => {
    return ({
        [RSAA]: {
            endpoint: `/api/v1/devices/${device_id}/commands?${queryParameters.join("&")}`,
            headers: JSONAPI_HEADERS,
            method: "GET",
            types: [
                COMMANDS_REQUEST,
                COMMANDS_SUCCESS,
                COMMANDS_FAILURE,
            ],
        },
    } as RSAAction<COMMANDS_REQUEST, COMMANDS_SUCCESS, COMMANDS_FAILURE>);
});

export const PATCH_REQUEST = "devices/PATCH_REQUEST";
export type PATCH_REQUEST = typeof PATCH_REQUEST;
export const PATCH_SUCCESS = "devices/PATCH_SUCCESS";
export type PATCH_SUCCESS = typeof PATCH_SUCCESS;
export const PATCH_FAILURE = "devices/PATCH_FAILURE";
export type PATCH_FAILURE = typeof PATCH_FAILURE;

export type PatchActionRequest = RSAAPatchActionRequest<PATCH_REQUEST, PATCH_SUCCESS, PATCH_FAILURE, Device>;
export type PatchActionResponse = RSAAReadActionResponse<PATCH_REQUEST, PATCH_SUCCESS, PATCH_FAILURE, JSONAPIDetailResponse<Device, Tag>>;

export const patch: PatchActionRequest = (deviceId: string, values: Device) => {

    return {
        [RSAA]: {
            body: JSON.stringify({
                data: {
                    attributes: values,
                    type: "devices",
                },
            }),
            endpoint: `/api/v1/devices/${deviceId}`,
            headers: JSONAPI_HEADERS,
            method: "PATCH",
            types: [
                PATCH_REQUEST,
                PATCH_SUCCESS,
                PATCH_FAILURE,
            ],
        },
    };
};

export const RPOST_REQUEST = "devices/RPOST_REQUEST";
export type RPOST_REQUEST = typeof RPOST_REQUEST;
export const RPOST_SUCCESS = "devices/RPOST_SUCCESS";
export type RPOST_SUCCESS = typeof RPOST_SUCCESS;
export const RPOST_FAILURE = "devices/RPOST_FAILURE";
export type RPOST_FAILURE = typeof RPOST_FAILURE;

type PostRelationshipActionRequest = (parentId: string, relationship: DeviceRelationship, data: JSONAPIRelationship[]) => RSAAction<RPOST_REQUEST, RPOST_SUCCESS, RPOST_FAILURE>;
export type PostRelationshipActionResponse = RSAAReadActionResponse<RPOST_REQUEST, RPOST_SUCCESS, RPOST_FAILURE, JSONAPIDetailResponse<Device, undefined>>;

export const postRelationship: PostRelationshipActionRequest = (id: string, relationship: DeviceRelationship, data: JSONAPIRelationship[]) => {
    return {
        [RSAA]: {
            body: JSON.stringify({ data }),
            endpoint: `/api/v1/devices/${id}/relationships/${relationship}`,
            headers: JSONAPI_HEADERS,
            method: "POST",
            types: [
                RPOST_REQUEST,
                RPOST_SUCCESS,
                RPOST_FAILURE,
            ],
        },
    };
};

export const RCPOST_REQUEST = "devices/RCPOST_REQUEST";
export type RCPOST_REQUEST = typeof RCPOST_REQUEST;
export const RCPOST_SUCCESS = "devices/RCPOST_SUCCESS";
export type RCPOST_SUCCESS = typeof RCPOST_SUCCESS;
export const RCPOST_FAILURE = "devices/RCPOST_FAILURE";
export type RCPOST_FAILURE = typeof RCPOST_FAILURE;

type PostRelatedActionRequest = <TRelated>(parentId: string, relationship: DeviceRelationship, data: TRelated) => RSAAction<RCPOST_REQUEST, RCPOST_SUCCESS, RCPOST_FAILURE>;
export type PostRelatedActionResponse = RSAAReadActionResponse<RCPOST_REQUEST, RCPOST_SUCCESS, RCPOST_FAILURE, JSONAPIDetailResponse<any, undefined>>;

export const postRelated: PostRelatedActionRequest = <TRelated>(parentId: string, relationship: DeviceRelationship, data: TRelated): RSAAction<RCPOST_REQUEST, RCPOST_SUCCESS, RCPOST_FAILURE> => {
    return {
        [RSAA]: {
            body: JSON.stringify({ data: {
                attributes: data,
                relationships: {
                    devices: {
                        data: [
                            {
                                id: parentId,
                                type: "devices",
                            },
                        ],
                    },
                },
                type: relationship,
            } }),
            endpoint: `/api/v1/devices/${parentId}/${relationship}`,
            headers: JSONAPI_HEADERS,
            method: "POST",
            types: [
                RCPOST_REQUEST,
                RCPOST_SUCCESS,
                RCPOST_FAILURE,
            ],
        },
    };
};

export const RPATCH_REQUEST = "devices/RPATCH_REQUEST";
export type RPATCH_REQUEST = typeof RPATCH_REQUEST;
export const RPATCH_SUCCESS = "devices/RPATCH_SUCCESS";
export type RPATCH_SUCCESS = typeof RPATCH_SUCCESS;
export const RPATCH_FAILURE = "devices/RPATCH_FAILURE";
export type RPATCH_FAILURE = typeof RPATCH_FAILURE;

type PatchRelationshipActionRequest = (parentId: string, relationship: DeviceRelationship, data: JSONAPIRelationship[]) => RSAAction<RPATCH_REQUEST, RPATCH_SUCCESS, RPATCH_FAILURE>;
export type PatchRelationshipActionResponse = RSAAReadActionResponse<RPATCH_REQUEST, RPATCH_SUCCESS, RPATCH_FAILURE, JSONAPIDetailResponse<Device, undefined>>;

export const patchRelationship: PatchRelationshipActionRequest = (id: string, relationship: DeviceRelationship, data: JSONAPIRelationship[]) => {
    return {
        [RSAA]: {
            body: JSON.stringify({ data }),
            endpoint: `/api/v1/devices/${id}/relationships/${relationship}`,
            headers: JSONAPI_HEADERS,
            method: "PATCH",
            types: [
                RPATCH_REQUEST,
                RPATCH_SUCCESS,
                RPATCH_FAILURE,
            ],
        },
    };
};
