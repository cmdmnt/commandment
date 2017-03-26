/// <reference path="../types/redux-api-middleware.d.ts" />
import { CALL_API, RSAA } from 'redux-api-middleware';
import { JSONAPI_HEADERS } from './constants'

export type INDEX_REQUEST = 'certificates/INDEX_REQUEST';
export const INDEX_REQUEST: INDEX_REQUEST = 'certificates/INDEX_REQUEST';
export type INDEX_SUCCESS = 'certificates/INDEX_SUCCESS';
export const INDEX_SUCCESS: INDEX_SUCCESS = 'certificates/INDEX_SUCCESS';
export type INDEX_FAILURE = 'certificates/INDEX_FAILURE';
export const INDEX_FAILURE: INDEX_FAILURE = 'certificates/INDEX_FAILURE';

export const index = (limit: number = 50, offset: number = 0, sort: Array<string> = [], filter: string): RSAA => {
    return {
        [CALL_API]: {
            endpoint: '/api/v1/certificates',
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
