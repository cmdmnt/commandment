import {Action, Dispatch} from "redux";
import {HTTPVerb, RSAA, RSAAction} from "redux-api-middleware";
import {ThunkAction} from "redux-thunk";
import {RootState} from "../../reducers/index";
import {JSON_HEADERS, JSONAPI_HEADERS} from "../constants"
import {
    JSONAPIRelationship, JSONAPIRelationships,
    RSAAChildIndexActionRequest,
    RSAAIndexActionRequest,
    RSAAIndexActionResponse, RSAAPatchActionRequest, RSAAReadActionRequest, RSAAReadActionResponse,
} from "../json-api";
import {JSONAPIDetailResponse, JSONAPIErrorResponse} from "../json-api";
import {Tag} from "../tags/types";
import {Command, Device, DeviceRelationship} from "./types";
import {
    encodeJSONAPIChildIndexParameters,
    encodeJSONAPIIndexParameters,
    FlaskFilter,
    FlaskFilters
} from "../../flask-rest-jsonapi";

export enum DevicesActionTypes {
    INDEX_REQUEST = "devices/INDEX_REQUEST",
    INDEX_SUCCESS = "devices/INDEX_SUCCESS",
    INDEX_FAILURE = "devices/INDEX_FAILURE",
    READ_REQUEST = "devices/READ_REQUEST",
    READ_SUCCESS = "devices/READ_SUCCESS",
    READ_FAILURE = "devices/READ_FAILURE",
    PATCH_REQUEST = "devices/PATCH_REQUEST",
    PATCH_SUCCESS = "devices/PATCH_SUCCESS",
    PATCH_FAILURE = "devices/PATCH_FAILURE",
    // Relationships
    COMMANDS_REQUEST = "devices/COMMANDS_REQUEST",
    COMMANDS_SUCCESS = "devices/COMMANDS_SUCCESS",
    COMMANDS_FAILURE = "devices/COMMANDS_FAILURE",
    REL_POST_REQUEST = "devices/REL_POST_REQUEST",
    REL_POST_SUCCESS = "devices/REL_POST_SUCCESS",
    REL_POST_FAILURE = "devices/REL_POST_FAILURE",
    // Interactive methods
    PUSH_REQUEST = "devices/PUSH_REQUEST",
    PUSH_SUCCESS = "devices/PUSH_SUCCESS",
    PUSH_FAILURE = "devices/PUSH_FAILURE",
    ERASE_REQUEST = "devices/ERASE_REQUEST",
    ERASE_SUCCESS = "devices/ERASE_SUCCESS",
    ERASE_FAILURE = "devices/ERASE_FAILURE",
    LOCK_REQUEST = "devices/LOCK_REQUEST",
    LOCK_SUCCESS = "devices/LOCK_SUCCESS",
    LOCK_FAILURE = "devices/LOCK_FAILURE",
    RESTART_REQUEST = "devices/RESTART_REQUEST",
    RESTART_SUCCESS = "devices/RESTART_SUCCESS",
    RESTART_FAILURE = "devices/RESTART_FAILURE",
    SHUTDOWN_REQUEST = "devices/SHUTDOWN_REQUEST",
    SHUTDOWN_SUCCESS = "devices/SHUTDOWN_SUCCESS",
    SHUTDOWN_FAILURE = "devices/SHUTDOWN_FAILURE",
    CLEARPASSCODE_REQUEST = "devices/CLEARPASSCODE_REQUEST",
    CLEARPASSCODE_SUCCESS = "devices/CLEARPASSCODE_SUCCESS",
    CLEARPASSCODE_FAILURE = "devices/CLEARPASSCODE_FAILURE",
    INVENTORY_REQUEST = "devices/INVENTORY_REQUEST",
    INVENTORY_SUCCESS = "devices/INVENTORY_SUCCESS",
    INVENTORY_FAILURE = "devices/INVENTORY_FAILURE",

}

export type IndexActionRequest = RSAAIndexActionRequest<DevicesActionTypes.INDEX_REQUEST, DevicesActionTypes.INDEX_SUCCESS, DevicesActionTypes.INDEX_FAILURE>;
export type IndexActionResponse = RSAAIndexActionResponse<DevicesActionTypes.INDEX_REQUEST, DevicesActionTypes.INDEX_SUCCESS, DevicesActionTypes.INDEX_FAILURE, Device>;

export const index = encodeJSONAPIIndexParameters((queryParameters: string[]) => {
    return ({
        [RSAA]: {
            endpoint: "/api/v1/devices?" + queryParameters.join("&"),
            headers: (state: RootState) => ({
                ...JSONAPI_HEADERS,
                Authorization: `Bearer ${state.auth.access_token}`,
            }),
            method: ("GET" as HTTPVerb),
            types: [
                DevicesActionTypes.INDEX_REQUEST,
                DevicesActionTypes.INDEX_SUCCESS,
                DevicesActionTypes.INDEX_FAILURE,
            ],
        },
    } as RSAAction<
        DevicesActionTypes.INDEX_REQUEST,
        DevicesActionTypes.INDEX_SUCCESS,
        DevicesActionTypes.INDEX_FAILURE>);
});

export const fetchDevicesIfRequired = (
        size: number = 10,
        pageNumber: number = 1,
        sort?: string[],
        filters?: FlaskFilters,
    ): ThunkAction<void, RootState, void, IndexActionResponse> => (dispatch: Dispatch, getState: () => RootState) => {

    const { auth: { access_token } } = getState();

    // const { devices } = getState();
    // if (devices.lastReceived) {
    //     const now = new Date();
    //     const seconds = 10;
    //     if ((now.getTime() - devices.lastReceived.getTime()) / 1000 < seconds) {
    //         console.log("cache hit");
    //         return;
    //     }
    // }

    dispatch(index(size, pageNumber, sort, filters));
};

export type ReadActionRequest = RSAAReadActionRequest<
    DevicesActionTypes.READ_REQUEST, DevicesActionTypes.READ_SUCCESS, DevicesActionTypes.READ_FAILURE>;
export type ReadActionResponse = RSAAReadActionResponse<
    DevicesActionTypes.READ_REQUEST,
    DevicesActionTypes.READ_SUCCESS,
    DevicesActionTypes.READ_FAILURE,
    JSONAPIDetailResponse<Device, undefined>>;

export const read: ReadActionRequest = (id: string, include?: string[]) => {

    let inclusions = "";
    if (include && include.length) {
        inclusions = "include=" + include.join(",")
    }

    return {
        [RSAA]: {
            endpoint: `/api/v1/devices/${id}?${inclusions}`,
            headers: (state: RootState) => ({
                ...JSONAPI_HEADERS,
                Authorization: `Bearer ${state.auth.access_token}`,
            }),
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

export type CacheFetchActionRequest = (id: string, include?: string[]) => ThunkAction<void, RootState, any, ReadActionResponse>;

export const fetchDeviceIfRequired = (
    id: string, include?: string[],
) => (
    dispatch: Dispatch,
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

export type PushActionRequest = (id: string | number) =>
    RSAAction<DevicesActionTypes.PUSH_REQUEST, DevicesActionTypes.PUSH_SUCCESS, DevicesActionTypes.PUSH_FAILURE>;

export interface PushActionResponse {
    type: DevicesActionTypes.PUSH_REQUEST | DevicesActionTypes.PUSH_SUCCESS | DevicesActionTypes.PUSH_FAILURE;
    payload?: JSONAPIDetailResponse<any, undefined> | JSONAPIErrorResponse;
}

export const push: PushActionRequest = (id: string | number) => {
    return {
        [RSAA]: {
            endpoint: `/api/v1/devices/${id}/push`,
            headers: (state: RootState) => ({
                ...JSONAPI_HEADERS,
                Authorization: `Bearer ${state.auth.access_token}`,
            }),
            method: "POST",
            types: [
                DevicesActionTypes.PUSH_REQUEST,
                DevicesActionTypes.PUSH_SUCCESS,
                DevicesActionTypes.PUSH_FAILURE,
            ],
        },
    }
};

export type RestartActionRequest = (id: string | number) => RSAAction<
    DevicesActionTypes.RESTART_REQUEST, DevicesActionTypes.RESTART_SUCCESS, DevicesActionTypes.RESTART_FAILURE>;

export interface RestartActionResponse {
    type: DevicesActionTypes.RESTART_REQUEST | DevicesActionTypes.RESTART_SUCCESS | DevicesActionTypes.RESTART_FAILURE;
    payload?: JSONAPIDetailResponse<any, undefined> | JSONAPIErrorResponse;
}

export const restart: RestartActionRequest = (deviceId: string | number) => {
    return {
        [RSAA]: {
            endpoint: `/api/v1/devices/${deviceId}/restart`,
            headers: (state: RootState) => ({
                ...JSONAPI_HEADERS,
                Authorization: `Bearer ${state.auth.access_token}`,
            }),
            method: "POST",
            types: [
                DevicesActionTypes.RESTART_REQUEST,
                DevicesActionTypes.RESTART_SUCCESS,
                DevicesActionTypes.RESTART_FAILURE,
            ],
        },
    }
};

export type ShutdownActionRequest = (id: string | number) =>
    RSAAction<
        DevicesActionTypes.SHUTDOWN_REQUEST,
        DevicesActionTypes.SHUTDOWN_SUCCESS,
        DevicesActionTypes.SHUTDOWN_FAILURE>;

export interface ShutdownActionResponse {
    type: DevicesActionTypes.SHUTDOWN_REQUEST |
          DevicesActionTypes.SHUTDOWN_SUCCESS |
          DevicesActionTypes.SHUTDOWN_FAILURE;
    payload?: JSONAPIDetailResponse<any, undefined> | JSONAPIErrorResponse;
}

export const shutdown: ShutdownActionRequest = (id: string | number) => {
    return {
        [RSAA]: {
            endpoint: `/api/v1/devices/${id}/shutdown`,
            headers: (state: RootState) => ({
                ...JSONAPI_HEADERS,
                Authorization: `Bearer ${state.auth.access_token}`,
            }),
            method: "POST",
            types: [
                DevicesActionTypes.SHUTDOWN_REQUEST,
                DevicesActionTypes.SHUTDOWN_SUCCESS,
                DevicesActionTypes.SHUTDOWN_FAILURE,
            ],
        },
    }
};

export type EraseActionRequest = (id: string | number) =>
    RSAAction<
        DevicesActionTypes.ERASE_REQUEST,
        DevicesActionTypes.ERASE_SUCCESS,
        DevicesActionTypes.ERASE_FAILURE>;

export interface EraseActionResponse {
    type: DevicesActionTypes.ERASE_REQUEST |
          DevicesActionTypes.ERASE_SUCCESS |
          DevicesActionTypes.ERASE_FAILURE;
    payload?: JSONAPIDetailResponse<any, undefined> | JSONAPIErrorResponse;
}

export const erase: EraseActionRequest = (id: string | number) => {
    return {
        [RSAA]: {
            endpoint: `/api/v1/devices/${id}/erase`,
            headers: (state: RootState) => ({
                ...JSONAPI_HEADERS,
                Authorization: `Bearer ${state.auth.access_token}`,
            }),
            method: "POST",
            types: [
                DevicesActionTypes.ERASE_REQUEST,
                DevicesActionTypes.ERASE_SUCCESS,
                DevicesActionTypes.ERASE_FAILURE,
            ],
        },
    }
};

export type LockActionRequest = (id: string | number, pin?: string, message?: string, phoneNumber?: string) =>
    RSAAction<
        DevicesActionTypes.LOCK_REQUEST,
        DevicesActionTypes.LOCK_SUCCESS,
        DevicesActionTypes.LOCK_FAILURE>;

export interface LockActionResponse {
    type: DevicesActionTypes.LOCK_REQUEST |
          DevicesActionTypes.LOCK_SUCCESS |
          DevicesActionTypes.LOCK_FAILURE;
    payload?: JSONAPIDetailResponse<any, undefined> | JSONAPIErrorResponse;
}

export const lock: LockActionRequest = (deviceId: string | number, pin?: string, message?: string, phoneNumber?: string) => {
    return {
        [RSAA]: {
            body: JSON.stringify({
                message,
                phoneNumber,
                pin,
            }),
            endpoint: `/api/v1/devices/${deviceId}/lock`,
            headers: (state: RootState) => ({
                ...JSONAPI_HEADERS,
                Authorization: `Bearer ${state.auth.access_token}`,
            }),
            method: "POST",
            types: [
                DevicesActionTypes.LOCK_REQUEST,
                DevicesActionTypes.LOCK_SUCCESS,
                DevicesActionTypes.LOCK_FAILURE,
            ],
        },
    }
};

export type ClearPasscodeActionRequest = (id: string | number) =>
    RSAAction<
        DevicesActionTypes.CLEARPASSCODE_REQUEST,
        DevicesActionTypes.CLEARPASSCODE_SUCCESS,
        DevicesActionTypes.CLEARPASSCODE_FAILURE>;

export interface ClearPasscodeActionResponse {
    type: DevicesActionTypes.CLEARPASSCODE_REQUEST |
          DevicesActionTypes.CLEARPASSCODE_SUCCESS |
          DevicesActionTypes.CLEARPASSCODE_FAILURE;
    payload?: JSONAPIDetailResponse<any, undefined> | JSONAPIErrorResponse;
}

export const clearPasscode: ClearPasscodeActionRequest = (id: string | number) => {
    return {
        [RSAA]: {
            endpoint: `/api/v1/devices/${id}/clear_passcode`,
            headers: (state: RootState) => ({
                ...JSONAPI_HEADERS,
                Authorization: `Bearer ${state.auth.access_token}`,
            }),
            method: "POST",
            types: [
                DevicesActionTypes.CLEARPASSCODE_REQUEST,
                DevicesActionTypes.CLEARPASSCODE_SUCCESS,
                DevicesActionTypes.CLEARPASSCODE_FAILURE,
            ],
        },
    }
};

export type InventoryActionRequest = (id: string | number) =>
    RSAAction<DevicesActionTypes.INVENTORY_REQUEST,
        DevicesActionTypes.INVENTORY_SUCCESS,
        DevicesActionTypes.INVENTORY_FAILURE>;

export interface InventoryActionResponse {
    type: DevicesActionTypes.INVENTORY_REQUEST |
          DevicesActionTypes.INVENTORY_SUCCESS |
          DevicesActionTypes.INVENTORY_FAILURE;
    payload?: JSONAPIDetailResponse<any, undefined> | JSONAPIErrorResponse;
}

export const inventory: InventoryActionRequest = (id: string | number) => {
    return {
        [RSAA]: {
            endpoint: `/api/v1/devices/inventory/${id}`,
            headers: (state: RootState) => ({
                ...JSONAPI_HEADERS,
                Authorization: `Bearer ${state.auth.access_token}`,
            }),
            method: "GET",
            types: [
                DevicesActionTypes.INVENTORY_REQUEST,
                DevicesActionTypes.INVENTORY_SUCCESS,
                DevicesActionTypes.INVENTORY_FAILURE,
            ],
        },
    }
};

export type TEST_REQUEST = "devices/TEST_REQUEST";
export const TEST_REQUEST: TEST_REQUEST = "devices/TEST_REQUEST";
export type TEST_SUCCESS = "devices/TEST_SUCCESS";
export const TEST_SUCCESS: TEST_SUCCESS = "devices/TEST_SUCCESS";
export type TEST_FAILURE = "devices/TEST_FAILURE";
export const TEST_FAILURE: TEST_FAILURE = "devices/TEST_FAILURE";

export type TestActionRequest = (id: string | number) => RSAAction<TEST_REQUEST, TEST_SUCCESS, TEST_FAILURE>;
export interface TestActionResponse {
    type: TEST_REQUEST | TEST_SUCCESS | TEST_FAILURE;
    payload?: JSONAPIDetailResponse<any, undefined> | JSONAPIErrorResponse;
}

export const test: TestActionRequest = (id: string | number) => {
    return {
        [RSAA]: {
            endpoint: `/api/v1/devices/test/${id}`,
            headers: (state: RootState) => ({
                ...JSONAPI_HEADERS,
                Authorization: `Bearer ${state.auth.access_token}`,
            }),
            method: "POST",
            types: [
                TEST_REQUEST,
                TEST_SUCCESS,
                TEST_FAILURE,
            ],
        },
    }
};

export type CommandsActionRequest = RSAAChildIndexActionRequest<
    DevicesActionTypes.COMMANDS_REQUEST, DevicesActionTypes.COMMANDS_SUCCESS, DevicesActionTypes.COMMANDS_FAILURE>;
export type CommandsActionResponse = RSAAIndexActionResponse<
    DevicesActionTypes.COMMANDS_REQUEST,
    DevicesActionTypes.COMMANDS_SUCCESS,
    DevicesActionTypes.COMMANDS_FAILURE,
    Command>;

export const commands = encodeJSONAPIChildIndexParameters((deviceId: string, queryParameters: string[])  => {
    return ({
        [RSAA]: {
            endpoint: `/api/v1/devices/${deviceId}/commands?${queryParameters.join("&")}`,
            headers: (state: RootState) => ({
                ...JSONAPI_HEADERS,
                Authorization: `Bearer ${state.auth.access_token}`,
            }),
            method: "GET",
            types: [
                DevicesActionTypes.COMMANDS_REQUEST,
                DevicesActionTypes.COMMANDS_SUCCESS,
                DevicesActionTypes.COMMANDS_FAILURE,
            ],
        },
    } as RSAAction<
        DevicesActionTypes.COMMANDS_REQUEST,
        DevicesActionTypes.COMMANDS_SUCCESS,
        DevicesActionTypes.COMMANDS_FAILURE>);
});

export type PatchActionRequest = RSAAPatchActionRequest<
    DevicesActionTypes.PATCH_REQUEST, DevicesActionTypes.PATCH_SUCCESS, DevicesActionTypes.PATCH_FAILURE, Device>;
export type PatchActionResponse = RSAAReadActionResponse<
    DevicesActionTypes.PATCH_REQUEST,
    DevicesActionTypes.PATCH_SUCCESS,
    DevicesActionTypes.PATCH_FAILURE,
    JSONAPIDetailResponse<Device, Tag>>;

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
            headers: (state: RootState) => ({
                ...JSONAPI_HEADERS,
                Authorization: `Bearer ${state.auth.access_token}`,
            }),
            method: "PATCH",
            types: [
                DevicesActionTypes.PATCH_REQUEST,
                DevicesActionTypes.PATCH_SUCCESS,
                DevicesActionTypes.PATCH_FAILURE,
            ],
        },
    }
};

type PostRelationshipActionRequest = (parentId: string, relationship: DeviceRelationship, data: JSONAPIRelationship[]) =>
    RSAAction<DevicesActionTypes.REL_POST_REQUEST, DevicesActionTypes.REL_POST_SUCCESS, DevicesActionTypes.REL_POST_FAILURE>;
export type PostRelationshipActionResponse = RSAAReadActionResponse<
    DevicesActionTypes.REL_POST_REQUEST,
    DevicesActionTypes.REL_POST_SUCCESS,
    DevicesActionTypes.REL_POST_FAILURE,
    JSONAPIDetailResponse<Device, undefined>>;

export const postRelationship: PostRelationshipActionRequest = (id: string, relationship: DeviceRelationship, data: JSONAPIRelationship[]) => {
    return {
        [RSAA]: {
            body: JSON.stringify({ data }),
            endpoint: `/api/v1/devices/${id}/relationships/${relationship}`,
            headers: (state: RootState) => ({
                ...JSONAPI_HEADERS,
                Authorization: `Bearer ${state.auth.access_token}`,
            }),
            method: "POST",
            types: [
                DevicesActionTypes.REL_POST_REQUEST,
                DevicesActionTypes.REL_POST_SUCCESS,
                DevicesActionTypes.REL_POST_FAILURE,
            ],
        },
    }
};

export const RCPOST_REQUEST = "devices/RCPOST_REQUEST";
export type RCPOST_REQUEST = typeof RCPOST_REQUEST;
export const RCPOST_SUCCESS = "devices/RCPOST_SUCCESS";
export type RCPOST_SUCCESS = typeof RCPOST_SUCCESS;
export const RCPOST_FAILURE = "devices/RCPOST_FAILURE";
export type RCPOST_FAILURE = typeof RCPOST_FAILURE;

export type PostRelatedActionRequest = <TRelated>(parentId: string, relationship: DeviceRelationship, data: TRelated) => RSAAction<RCPOST_REQUEST, RCPOST_SUCCESS, RCPOST_FAILURE>;
export type PostRelatedActionResponse = RSAAReadActionResponse<RCPOST_REQUEST, RCPOST_SUCCESS, RCPOST_FAILURE, JSONAPIDetailResponse<any, undefined>>;

export const postRelated: PostRelatedActionRequest = <TRelated>(
    parentId: string,
    relationship: DeviceRelationship,
    data: TRelated): RSAAction<RCPOST_REQUEST, RCPOST_SUCCESS, RCPOST_FAILURE> => {
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
            headers: (state: RootState) => ({
                ...JSONAPI_HEADERS,
                Authorization: `Bearer ${state.auth.access_token}`,
            }),
            method: "POST",
            types: [
                RCPOST_REQUEST,
                RCPOST_SUCCESS,
                RCPOST_FAILURE,
            ],
        },
    }
};

export const RPATCH_REQUEST = "devices/RPATCH_REQUEST";
export type RPATCH_REQUEST = typeof RPATCH_REQUEST;
export const RPATCH_SUCCESS = "devices/RPATCH_SUCCESS";
export type RPATCH_SUCCESS = typeof RPATCH_SUCCESS;
export const RPATCH_FAILURE = "devices/RPATCH_FAILURE";
export type RPATCH_FAILURE = typeof RPATCH_FAILURE;

export type PatchRelationshipActionRequest = (
    parentId: string,
    relationship: DeviceRelationship,
    data: JSONAPIRelationship[]) => RSAAction<RPATCH_REQUEST, RPATCH_SUCCESS, RPATCH_FAILURE>;

export type PatchRelationshipActionResponse = RSAAReadActionResponse<
    RPATCH_REQUEST, RPATCH_SUCCESS, RPATCH_FAILURE, JSONAPIDetailResponse<Device, undefined>>;

export const patchRelationship: PatchRelationshipActionRequest = (
    id: string, relationship: DeviceRelationship, data: JSONAPIRelationship[]) => {
    return {
        [RSAA]: {
            body: JSON.stringify({ data }),
            endpoint: `/api/v1/devices/${id}/relationships/${relationship}`,
            headers: (state: RootState) => ({
                ...JSONAPI_HEADERS,
                Authorization: `Bearer ${state.auth.access_token}`,
            }),
            method: "PATCH",
            types: [
                RPATCH_REQUEST,
                RPATCH_SUCCESS,
                RPATCH_FAILURE,
            ],
        },
    }
};
