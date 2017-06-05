/// <reference path="../typings/redux-api-middleware.d.ts" />
import { CALL_API, RSAA } from 'redux-api-middleware';
import {JSONAPI_HEADERS, FlaskFilters, FlaskFilter, JSON_HEADERS} from './constants'
import {
    encodeJSONAPIChildIndexParameters, encodeJSONAPIIndexParameters, JSONAPIDetailResponse, JSONAPIListResponse,
    JSONAPIObject,
    RSAAIndexActionRequest,
    RSAAIndexActionResponse, RSAAReadActionRequest, RSAAReadActionResponse
} from "../json-api";
import {Device, DeviceGroup} from "../models";


export type INDEX_REQUEST = 'device_groups/INDEX_REQUEST';
export const INDEX_REQUEST: INDEX_REQUEST = 'device_groups/INDEX_REQUEST';
export type INDEX_SUCCESS = 'device_groups/INDEX_SUCCESS';
export const INDEX_SUCCESS: INDEX_SUCCESS = 'device_groups/INDEX_SUCCESS';
export type INDEX_FAILURE = 'device_groups/INDEX_FAILURE';
export const INDEX_FAILURE: INDEX_FAILURE = 'device_groups/INDEX_FAILURE';

export type IndexActionRequest = RSAAIndexActionRequest<INDEX_REQUEST, INDEX_SUCCESS, INDEX_FAILURE>;
export type IndexActionResponse = RSAAIndexActionResponse<INDEX_REQUEST, INDEX_SUCCESS, INDEX_FAILURE, DeviceGroup>;

export const index = encodeJSONAPIIndexParameters((queryParameters: Array<String>) => {
    return {
        [CALL_API]: {
            endpoint: '/api/v1/device_groups?' + queryParameters.join('&'),
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

export type READ_REQUEST = 'device_groups/READ_REQUEST';
export const READ_REQUEST: READ_REQUEST = 'device_groups/READ_REQUEST';
export type READ_SUCCESS = 'device_groups/READ_SUCCESS';
export const READ_SUCCESS: READ_SUCCESS = 'device_groups/READ_SUCCESS';
export type READ_FAILURE = 'device_groups/READ_FAILURE';
export const READ_FAILURE: READ_FAILURE = 'device_groups/READ_FAILURE';

export type ReadActionRequest = RSAAReadActionRequest<READ_REQUEST, READ_SUCCESS, READ_FAILURE>;
export type ReadActionResponse = RSAAReadActionResponse<READ_REQUEST, READ_SUCCESS, READ_FAILURE, JSONAPIDetailResponse<DeviceGroup, undefined>>;

export const read: ReadActionRequest = (id: string, include?: Array<string>) => {

    let inclusions = '';
    if (include && include.length) {
        inclusions = 'include=' + include.join(',')
    }

    return {
        [CALL_API]: {
            endpoint: `/api/v1/device_groups/${id}?${inclusions}`,
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


export type POST_REQUEST = 'device_groups/POST_REQUEST';
export const POST_REQUEST: POST_REQUEST = 'device_groups/POST_REQUEST';
export type POST_SUCCESS = 'device_groups/POST_SUCCESS';
export const POST_SUCCESS: POST_SUCCESS = 'device_groups/POST_SUCCESS';
export type POST_FAILURE = 'device_groups/POST_FAILURE';
export const POST_FAILURE: POST_FAILURE = 'device_groups/POST_FAILURE';

export interface PostActionRequest {
    (values: DeviceGroup): RSAA<POST_REQUEST, POST_SUCCESS, POST_FAILURE>;
}

export interface PostActionResponse {
    type: POST_REQUEST | POST_FAILURE | POST_SUCCESS;
    payload?: JSONAPIListResponse<JSONAPIObject<DeviceGroup>>;
}

export const post: PostActionRequest = (values: DeviceGroup) => {

    return {
        [CALL_API]: {
            endpoint: `/api/v1/device_groups`,
            method: 'POST',
            types: [
                POST_REQUEST,
                POST_SUCCESS,
                POST_FAILURE
            ],
            headers: JSONAPI_HEADERS,
            body: JSON.stringify({
                data: {
                    type: "device_groups",
                    attributes: values
                }
            })
        }
    }
};