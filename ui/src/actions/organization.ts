/// <reference path="../typings/redux-api-middleware.d.ts" />
import { CALL_API, RSAA } from 'redux-api-middleware';
import {JSONAPI_HEADERS, FlaskFilters, FlaskFilter} from './constants'

export type INDEX_REQUEST = 'organizations/INDEX_REQUEST';
export const INDEX_REQUEST: INDEX_REQUEST = 'organizations/INDEX_REQUEST';
export type INDEX_SUCCESS = 'organizations/INDEX_SUCCESS';
export const INDEX_SUCCESS: INDEX_SUCCESS = 'organizations/INDEX_SUCCESS';
export type INDEX_FAILURE = 'organizations/INDEX_FAILURE';
export const INDEX_FAILURE: INDEX_FAILURE = 'organizations/INDEX_FAILURE';

export interface IndexActionRequest {
    (size?: number, number?: number, sort?: Array<string>, filter?: Array<FlaskFilter>): RSAA<INDEX_REQUEST, INDEX_SUCCESS, INDEX_FAILURE>;
}

export interface IndexActionResponse {
    type: INDEX_REQUEST | INDEX_FAILURE | INDEX_SUCCESS;
    payload?: JSONAPIListResponse<JSONAPIObject<Organization>>;
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
            endpoint: '/api/v1/organizations/?' + queryParameters.join('&'),
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

export type POST_REQUEST = 'organizations/POST_REQUEST';
export const POST_REQUEST: POST_REQUEST = 'organizations/POST_REQUEST';
export type POST_SUCCESS = 'organizations/POST_SUCCESS';
export const POST_SUCCESS: POST_SUCCESS = 'organizations/POST_SUCCESS';
export type POST_FAILURE = 'organizations/POST_FAILURE';
export const POST_FAILURE: POST_FAILURE = 'organizations/POST_FAILURE';

export interface PostActionRequest {
    (values: Organization): RSAA<POST_REQUEST, POST_SUCCESS, POST_FAILURE>;
}

export interface PostActionResponse {
    type: POST_REQUEST | POST_FAILURE | POST_SUCCESS;
    payload?: JSONAPIListResponse<JSONAPIObject<Organization>>;
}

export const post: PostActionRequest = (values: Organization) => {
    return {
        [CALL_API]: {
            endpoint: `/api/v1/organizations`,
            method: 'POST',
            types: [
                POST_REQUEST,
                POST_SUCCESS,
                POST_FAILURE
            ],
            headers: JSONAPI_HEADERS,
            body: JSON.stringify({
                data: {
                    type: "organizations",
                    attributes: values
                }
            })
        }
    }
};
