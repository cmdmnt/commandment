/// <reference path="../typings/redux-api-middleware.d.ts" />
import { CALL_API, RSAA } from 'redux-api-middleware';
import {JSONAPI_HEADERS, FlaskFilters, FlaskFilter, JSON_HEADERS} from './constants'
import {
    encodeJSONAPIChildIndexParameters, encodeJSONAPIIndexParameters, RSAAIndexActionRequest,
    RSAAIndexActionResponse, RSAAReadActionRequest, RSAAReadActionResponse
} from "../json-api";
import {Command, Device} from "../models";
import {JSONAPIDetailResponse, JSONAPIErrorResponse} from "../json-api";
import {ThunkAction} from "redux-thunk";
import {RootState} from "../reducers/index";





export type INDEX_REQUEST = 'devices/INDEX_REQUEST';
export const INDEX_REQUEST: INDEX_REQUEST = 'devices/INDEX_REQUEST';
export type INDEX_SUCCESS = 'devices/INDEX_SUCCESS';
export const INDEX_SUCCESS: INDEX_SUCCESS = 'devices/INDEX_SUCCESS';
export type INDEX_FAILURE = 'devices/INDEX_FAILURE';
export const INDEX_FAILURE: INDEX_FAILURE = 'devices/INDEX_FAILURE';

export type IndexActionRequest = RSAAIndexActionRequest<INDEX_REQUEST, INDEX_SUCCESS, INDEX_FAILURE>;
export type IndexActionResponse = RSAAIndexActionResponse<INDEX_REQUEST, INDEX_SUCCESS, INDEX_FAILURE, Device>;

export const index = encodeJSONAPIIndexParameters((queryParameters: Array<String>) => {
    return {
        [CALL_API]: {
            endpoint: '/api/v1/devices?' + queryParameters.join('&'),
            method: 'GET',
            types: [
                INDEX_REQUEST,
                INDEX_SUCCESS,
                INDEX_FAILURE
            ],
            headers: JSONAPI_HEADERS
        }
    }
});

export const fetchDevicesIfRequired: ThunkAction<void, RootState, {}> = (
        size: number = 10,
        pageNumber: number = 1,
        sort?: Array<string>,
        filters?: FlaskFilters
    ) => (dispatch, getState) => {

    const { devices } = getState();
    if (devices.lastReceived) {
        const now = new Date();
        const seconds = 10;
        if ((now.getTime() - devices.lastReceived.getTime()) / 1000 < seconds) {
            console.log('cache hit');
            return;
        }
    }

    dispatch(index(size, pageNumber, sort, filters));
};


export type READ_REQUEST = 'devices/READ_REQUEST';
export const READ_REQUEST: READ_REQUEST = 'devices/READ_REQUEST';
export type READ_SUCCESS = 'devices/READ_SUCCESS';
export const READ_SUCCESS: READ_SUCCESS = 'devices/READ_SUCCESS';
export type READ_FAILURE = 'devices/READ_FAILURE';
export const READ_FAILURE: READ_FAILURE = 'devices/READ_FAILURE';

export type ReadActionRequest = RSAAReadActionRequest<READ_REQUEST, READ_SUCCESS, READ_FAILURE>;
export type ReadActionResponse = RSAAReadActionResponse<READ_REQUEST, READ_SUCCESS, READ_FAILURE, JSONAPIDetailResponse<Device, undefined>>;

export const read: ReadActionRequest = (id: number, include?: Array<string>) => {

    let inclusions = '';
    if (include && include.length) {
        inclusions = 'include=' + include.join(',')
    }

    return {
        [CALL_API]: {
            endpoint: `/api/v1/devices/${id}?${inclusions}`,
            method: 'GET',
            types: [
                READ_REQUEST,
                READ_SUCCESS,
                READ_FAILURE
            ],
            headers: JSONAPI_HEADERS
        }
    }
};


export type PUSH_REQUEST = 'devices/PUSH_REQUEST';
export const PUSH_REQUEST: PUSH_REQUEST = 'devices/PUSH_REQUEST';
export type PUSH_SUCCESS = 'devices/PUSH_SUCCESS';
export const PUSH_SUCCESS: PUSH_SUCCESS = 'devices/PUSH_SUCCESS';
export type PUSH_FAILURE = 'devices/PUSH_FAILURE';
export const PUSH_FAILURE: PUSH_FAILURE = 'devices/PUSH_FAILURE';

export interface PushActionRequest {
    (id: string): RSAA<PUSH_REQUEST, PUSH_SUCCESS, PUSH_FAILURE>;
}

export interface PushActionResponse {
    type: PUSH_REQUEST | PUSH_SUCCESS | PUSH_FAILURE;
    payload?: JSONAPIDetailResponse<any, undefined> | JSONAPIErrorResponse;
}

export const push: PushActionRequest = (id: string) => {
    return {
        [CALL_API]: {
            endpoint: `/api/v1/devices/${id}/push`,
            method: 'POST',
            types: [
                PUSH_REQUEST,
                PUSH_SUCCESS,
                PUSH_FAILURE
            ],
            headers: JSON_HEADERS
        }
    }
};

export type INVENTORY_REQUEST = 'devices/INVENTORY_REQUEST';
export const INVENTORY_REQUEST: INVENTORY_REQUEST = 'devices/INVENTORY_REQUEST';
export type INVENTORY_SUCCESS = 'devices/INVENTORY_SUCCESS';
export const INVENTORY_SUCCESS: INVENTORY_SUCCESS = 'devices/INVENTORY_SUCCESS';
export type INVENTORY_FAILURE = 'devices/INVENTORY_FAILURE';
export const INVENTORY_FAILURE: INVENTORY_FAILURE = 'devices/INVENTORY_FAILURE';

export interface InventoryActionRequest {
    (id: string): RSAA<INVENTORY_REQUEST, INVENTORY_SUCCESS, INVENTORY_FAILURE>;
}

export interface InventoryActionResponse {
    type: INVENTORY_REQUEST | INVENTORY_SUCCESS | INVENTORY_FAILURE;
    payload?: JSONAPIDetailResponse<any, undefined> | JSONAPIErrorResponse;
}

export const inventory: InventoryActionRequest = (id: string) => {
    return {
        [CALL_API]: {
            endpoint: `/api/v1/devices/inventory/${id}`,
            method: 'GET',
            types: [
                INVENTORY_REQUEST,
                INVENTORY_SUCCESS,
                INVENTORY_FAILURE
            ],
            headers: JSON_HEADERS
        }
    }
};


export type TEST_REQUEST = 'devices/TEST_REQUEST';
export const TEST_REQUEST: TEST_REQUEST = 'devices/TEST_REQUEST';
export type TEST_SUCCESS = 'devices/TEST_SUCCESS';
export const TEST_SUCCESS: TEST_SUCCESS = 'devices/TEST_SUCCESS';
export type TEST_FAILURE = 'devices/TEST_FAILURE';
export const TEST_FAILURE: TEST_FAILURE = 'devices/TEST_FAILURE';

export interface TestActionRequest {
    (id: string): RSAA<TEST_REQUEST, TEST_SUCCESS, TEST_FAILURE>;
}

export interface TestActionResponse {
    type: TEST_REQUEST | TEST_SUCCESS | TEST_FAILURE;
    payload?: JSONAPIDetailResponse<any, undefined> | JSONAPIErrorResponse;
}

export const test: TestActionRequest = (id: string) => {
    return {
        [CALL_API]: {
            endpoint: `/api/v1/devices/test/${id}`,
            method: 'POST',
            types: [
                TEST_REQUEST,
                TEST_SUCCESS,
                TEST_FAILURE
            ],
            headers: JSON_HEADERS
        }
    }
};

export type COMMANDS_REQUEST = 'devices/COMMANDS_REQUEST';
export const COMMANDS_REQUEST: COMMANDS_REQUEST = 'devices/COMMANDS_REQUEST';
export type COMMANDS_SUCCESS = 'devices/COMMANDS_SUCCESS';
export const COMMANDS_SUCCESS: COMMANDS_SUCCESS = 'devices/COMMANDS_SUCCESS';
export type COMMANDS_FAILURE = 'devices/COMMANDS_FAILURE';
export const COMMANDS_FAILURE: COMMANDS_FAILURE = 'devices/COMMANDS_FAILURE';

export type CommandsActionRequest = RSAAIndexActionRequest<COMMANDS_REQUEST, COMMANDS_SUCCESS, COMMANDS_FAILURE>;
export type CommandsActionResponse = RSAAIndexActionResponse<COMMANDS_REQUEST, COMMANDS_SUCCESS, COMMANDS_FAILURE, Command>;

export const commands = encodeJSONAPIChildIndexParameters((device_id: number, queryParameters: Array<String>)  => {
    return {
        [CALL_API]: {
            endpoint: `/api/v1/devices/${device_id}/commands?${queryParameters.join('&')}`,
            method: 'GET',
            types: [
                COMMANDS_REQUEST,
                COMMANDS_SUCCESS,
                COMMANDS_FAILURE
            ],
            headers: JSONAPI_HEADERS
        }
    }
});


