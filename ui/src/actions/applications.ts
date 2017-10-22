import {RSAA, HTTPVerb, RSAAction} from 'redux-api-middleware';
import {JSONAPI_HEADERS, FlaskFilters, FlaskFilter, JSON_HEADERS} from './constants'
import {
    encodeJSONAPIChildIndexParameters, encodeJSONAPIIndexParameters, JSONAPIListResponse, JSONAPIObject,
    RSAAIndexActionRequest,
    RSAAIndexActionResponse, RSAAPostActionRequest, RSAAPostActionResponse, RSAAReadActionRequest,
    RSAAReadActionResponse
} from "../json-api";
import {Application} from "../models";
import {JSONAPIDetailResponse, JSONAPIErrorResponse} from "../json-api";


export const POST_REQUEST = 'applications/POST_REQUEST';
export type POST_REQUEST = typeof POST_REQUEST;
export const POST_SUCCESS = 'applications/POST_SUCCESS';
export type POST_SUCCESS = typeof POST_SUCCESS;
export const POST_FAILURE = 'applications/POST_FAILURE';
export type POST_FAILURE = typeof POST_FAILURE;

export type PostActionRequest = RSAAPostActionRequest<POST_REQUEST, POST_SUCCESS, POST_FAILURE, Application>;
export type PostActionResponse = RSAAPostActionResponse<POST_REQUEST, POST_SUCCESS, POST_FAILURE, JSONAPIDetailResponse<Application, undefined>>;

export const post: PostActionRequest = (values: Application) => {

    return (<RSAAction<POST_REQUEST, POST_SUCCESS, POST_FAILURE>>{
        [RSAA]: {
            endpoint: `/api/v1/applications`,
            method: 'POST',
            types: [
                POST_REQUEST,
                POST_SUCCESS,
                POST_FAILURE
            ],
            headers: JSONAPI_HEADERS,
            body: JSON.stringify({
                data: {
                    type: "applications",
                    attributes: values
                }
            })
        }
    });
};