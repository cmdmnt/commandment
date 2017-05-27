/// <reference path="../typings/redux-api-middleware.d.ts" />
import { CALL_API, RSAA } from 'redux-api-middleware';
import {JSONAPI_HEADERS, JSON_HEADERS} from './constants'
import {RSAAReadActionRequest, RSAAReadActionResponse} from "../constants";
import {JSONAPIDetailResponse, Organization} from "../typings/definitions";

export type READ_REQUEST = 'organization/READ_REQUEST';
export const READ_REQUEST: READ_REQUEST = 'organization/READ_REQUEST';
export type READ_SUCCESS = 'organization/READ_SUCCESS';
export const READ_SUCCESS: READ_SUCCESS = 'organization/READ_SUCCESS';
export type READ_FAILURE = 'organization/READ_FAILURE';
export const READ_FAILURE: READ_FAILURE = 'organization/READ_FAILURE';

export type ReadActionRequest = RSAAReadActionRequest<READ_REQUEST, READ_SUCCESS, READ_FAILURE>;
export type ReadActionResponse = RSAAReadActionResponse<READ_REQUEST, READ_SUCCESS, READ_FAILURE, Organization>;

export const read: ReadActionRequest = () => {
    return {
        [CALL_API]: {
            endpoint: '/api/v1/configuration/organization',
            method: 'GET',
            types: [
                READ_REQUEST,
                READ_SUCCESS,
                READ_FAILURE
            ],
            headers: JSON_HEADERS
        }
    }
};

export type POST_REQUEST = 'organization/POST_REQUEST';
export const POST_REQUEST: POST_REQUEST = 'organization/POST_REQUEST';
export type POST_SUCCESS = 'organization/POST_SUCCESS';
export const POST_SUCCESS: POST_SUCCESS = 'organization/POST_SUCCESS';
export type POST_FAILURE = 'organization/POST_FAILURE';
export const POST_FAILURE: POST_FAILURE = 'organization/POST_FAILURE';

export interface PostActionRequest {
    (values: Organization): RSAA<POST_REQUEST, POST_SUCCESS, POST_FAILURE>;
}

export interface PostActionResponse {
    type: POST_REQUEST | POST_FAILURE | POST_SUCCESS;
    payload?: Organization;
}

export const post: PostActionRequest = (values: Organization) => {
    return {
        [CALL_API]: {
            endpoint: '/api/v1/configuration/organization',
            method: 'POST',
            types: [
                POST_REQUEST,
                POST_SUCCESS,
                POST_FAILURE
            ],
            headers: JSON_HEADERS,
            body: JSON.stringify(values)
        }
    }
};
