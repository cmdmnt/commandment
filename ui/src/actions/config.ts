/// <reference path="../typings/redux-api-middleware.d.ts" />
import { CALL_API, RSAA } from 'redux-api-middleware';
import {JSONAPI_HEADERS, FlaskFilters, FlaskFilter} from './constants'

export type POST_REQUEST = 'config/POST_REQUEST';
export const POST_REQUEST: POST_REQUEST = 'config/POST_REQUEST';
export type POST_SUCCESS = 'config/POST_SUCCESS';
export const POST_SUCCESS: POST_SUCCESS = 'config/POST_SUCCESS';
export type POST_FAILURE = 'config/POST_FAILURE';
export const POST_FAILURE: POST_FAILURE = 'config/POST_FAILURE';

export interface PostActionRequest {
    (values: MDMConfig): RSAA<POST_REQUEST, POST_SUCCESS, POST_FAILURE>;
}

export interface PostActionResponse {
    type: POST_REQUEST | POST_FAILURE | POST_SUCCESS;
    payload?: JSONAPIListResponse<JSONAPIObject<MDMConfig>>;
}

export const post: PostActionRequest = (values: MDMConfig) => {
    return {
        [CALL_API]: {
            endpoint: `/api/v1/config`,
            method: 'POST',
            types: [
                POST_REQUEST,
                POST_SUCCESS,
                POST_FAILURE
            ],
            headers: JSONAPI_HEADERS
        }
    }
};
