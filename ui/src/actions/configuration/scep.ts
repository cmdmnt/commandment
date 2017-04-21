/// <reference path="../../typings/redux-api-middleware.d.ts" />
import { CALL_API, RSAA } from 'redux-api-middleware';
import {JSONAPI_HEADERS, JSON_HEADERS} from '../constants'

export type READ_REQUEST = 'scep/READ_REQUEST';
export const READ_REQUEST: READ_REQUEST = 'scep/READ_REQUEST';
export type READ_SUCCESS = 'scep/READ_SUCCESS';
export const READ_SUCCESS: READ_SUCCESS = 'scep/READ_SUCCESS';
export type READ_FAILURE = 'scep/READ_FAILURE';
export const READ_FAILURE: READ_FAILURE = 'scep/READ_FAILURE';

export interface ReadActionRequest {
    (): RSAA<READ_REQUEST, READ_SUCCESS, READ_FAILURE>;
}

export interface ReadActionResponse {
    type: READ_REQUEST | READ_SUCCESS | READ_FAILURE;
    payload?: SCEPConfiguration;
}

export const read: ReadActionRequest = () => {
    return {
        [CALL_API]: {
            endpoint: '/api/v1/configuration/scep',
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

export type POST_REQUEST = 'scep/POST_REQUEST';
export const POST_REQUEST: POST_REQUEST = 'scep/POST_REQUEST';
export type POST_SUCCESS = 'scep/POST_SUCCESS';
export const POST_SUCCESS: POST_SUCCESS = 'scep/POST_SUCCESS';
export type POST_FAILURE = 'scep/POST_FAILURE';
export const POST_FAILURE: POST_FAILURE = 'scep/POST_FAILURE';

export interface PostActionRequest {
    (values: SCEPConfiguration): RSAA<POST_REQUEST, POST_SUCCESS, POST_FAILURE>;
}

export interface PostActionResponse {
    type: POST_REQUEST | POST_FAILURE | POST_SUCCESS;
    payload?: SCEPConfiguration;
}

export const post: PostActionRequest = (values: SCEPConfiguration) => {
    return {
        [CALL_API]: {
            endpoint: '/api/v1/configuration/scep',
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
