/// <reference path="../typings/redux-api-middleware.d.ts" />
import { CALL_API, RSAA } from 'redux-api-middleware';
import {JSONAPI_HEADERS, FlaskFilters, FlaskFilter, JSON_HEADERS} from './constants'
import {
    encodeJSONAPIChildIndexParameters, encodeJSONAPIIndexParameters, RSAAIndexActionRequest,
    RSAAIndexActionResponse, RSAAReadActionRequest, RSAAReadActionResponse
} from "../json-api";
import {Tag} from "../models";
import {JSONAPIDetailResponse, JSONAPIErrorResponse} from "../json-api";


export type INDEX_REQUEST = 'tags/INDEX_REQUEST';
export const INDEX_REQUEST: INDEX_REQUEST = 'tags/INDEX_REQUEST';
export type INDEX_SUCCESS = 'tags/INDEX_SUCCESS';
export const INDEX_SUCCESS: INDEX_SUCCESS = 'tags/INDEX_SUCCESS';
export type INDEX_FAILURE = 'tags/INDEX_FAILURE';
export const INDEX_FAILURE: INDEX_FAILURE = 'tags/INDEX_FAILURE';

export type IndexActionRequest = RSAAIndexActionRequest<INDEX_REQUEST, INDEX_SUCCESS, INDEX_FAILURE>;
export type IndexActionResponse = RSAAIndexActionResponse<INDEX_REQUEST, INDEX_SUCCESS, INDEX_FAILURE, Tag>;

export const index = encodeJSONAPIIndexParameters((queryParameters: Array<String>) => {
    return {
        [CALL_API]: {
            endpoint: '/api/v1/tags?' + queryParameters.join('&'),
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