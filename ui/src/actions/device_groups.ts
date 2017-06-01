/// <reference path="../typings/redux-api-middleware.d.ts" />
import { CALL_API, RSAA } from 'redux-api-middleware';
import {JSONAPI_HEADERS, FlaskFilters, FlaskFilter, JSON_HEADERS} from './constants'
import {
    encodeJSONAPIChildIndexParameters, encodeJSONAPIIndexParameters, RSAAIndexActionRequest,
    RSAAIndexActionResponse, RSAAReadActionRequest, RSAAReadActionResponse
} from "../json-api";
import {DeviceGroup} from "../models";


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