/// <reference path="../typings/redux-api-middleware.d.ts" />
import { CALL_API, RSAA } from 'redux-api-middleware';
import {JSONAPI_HEADERS, FlaskFilters, FlaskFilter, JSON_HEADERS} from './constants'

export type INDEX_REQUEST = 'devices/INDEX_REQUEST';
export const INDEX_REQUEST: INDEX_REQUEST = 'devices/INDEX_REQUEST';
export type INDEX_SUCCESS = 'devices/INDEX_SUCCESS';
export const INDEX_SUCCESS: INDEX_SUCCESS = 'devices/INDEX_SUCCESS';
export type INDEX_FAILURE = 'devices/INDEX_FAILURE';
export const INDEX_FAILURE: INDEX_FAILURE = 'devices/INDEX_FAILURE';

export interface IndexActionRequest {
    (size?: number, number?: number, sort?: Array<string>, filter?: Array<FlaskFilter>): RSAA<INDEX_REQUEST, INDEX_SUCCESS, INDEX_FAILURE>;
}

export interface IndexActionResponse {
    type: INDEX_REQUEST | INDEX_FAILURE | INDEX_SUCCESS;
    payload?: JSONAPIListResponse<JSONAPIObject<Device>>;
}

export const index: IndexActionRequest = (
    size: number = 50,
    number: number = 1,
    sort: Array<string> = [],
    filter?: Array<FlaskFilter>
): RSAA<INDEX_REQUEST, INDEX_SUCCESS, INDEX_FAILURE> => {

    let queryParameters = [];
    queryParameters.push(`size=${size}`);
    queryParameters.push(`number=${number}`);

    if (sort.length > 0) {
        // TODO: sorting
    }

    if (filter && filter.length > 0) {
        let rawFilters = JSON.stringify(filter);
        queryParameters.push(`filter=${rawFilters}`);
    }

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
};


export type READ_REQUEST = 'devices/READ_REQUEST';
export const READ_REQUEST: READ_REQUEST = 'devices/READ_REQUEST';
export type READ_SUCCESS = 'devices/READ_SUCCESS';
export const READ_SUCCESS: READ_SUCCESS = 'devices/READ_SUCCESS';
export type READ_FAILURE = 'devices/READ_FAILURE';
export const READ_FAILURE: READ_FAILURE = 'devices/READ_FAILURE';

export interface ReadActionRequest {
    (id: number, include?: Array<string>): RSAA<READ_REQUEST, READ_SUCCESS, READ_FAILURE>;
}

export interface ReadActionResponse {
    type: READ_REQUEST | READ_FAILURE | READ_SUCCESS;
    payload?: JSONAPIDetailResponse<Device>;
}

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
    (id: number): RSAA<PUSH_REQUEST, PUSH_SUCCESS, PUSH_FAILURE>;
}

export interface PushActionResponse {
    type: PUSH_REQUEST | PUSH_SUCCESS | PUSH_FAILURE;
    payload?: JSONAPIDetailResponse<any>;
}

export const push: PushActionRequest = (id: number) => {
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
    (id: number): RSAA<INVENTORY_REQUEST, INVENTORY_SUCCESS, INVENTORY_FAILURE>;
}

export interface InventoryActionResponse {
    type: INVENTORY_REQUEST | INVENTORY_SUCCESS | INVENTORY_FAILURE;
    payload?: JSONAPIDetailResponse<any>;
}

export const inventory: InventoryActionRequest = (id: number) => {
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