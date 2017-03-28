/// <reference path="../typings/redux-api-middleware.d.ts" />
import { CALL_API, RSAA } from 'redux-api-middleware';
import {JSONAPI_HEADERS, FlaskFilters, FlaskFilter} from './constants'

export type INDEX_REQUEST = 'certificates/INDEX_REQUEST';
export const INDEX_REQUEST: INDEX_REQUEST = 'certificates/INDEX_REQUEST';
export type INDEX_SUCCESS = 'certificates/INDEX_SUCCESS';
export const INDEX_SUCCESS: INDEX_SUCCESS = 'certificates/INDEX_SUCCESS';
export type INDEX_FAILURE = 'certificates/INDEX_FAILURE';
export const INDEX_FAILURE: INDEX_FAILURE = 'certificates/INDEX_FAILURE';

export interface IndexAction {
    (size: number, number: number, sort: Array<string>, filter?: Array<FlaskFilter>): RSAA<INDEX_REQUEST, INDEX_SUCCESS, INDEX_FAILURE>;
}

export const index: IndexAction = (
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
            endpoint: '/api/v1/certificates?' + queryParameters.join('&'),
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

export type PUSHCERT_REQUEST = 'certificates/PUSHCERT_REQUEST';
export const PUSHCERT_REQUEST: PUSHCERT_REQUEST = 'certificates/PUSHCERT_REQUEST';
export type PUSHCERT_SUCCESS = 'certificates/PUSHCERT_SUCCESS';
export const PUSHCERT_SUCCESS: PUSHCERT_SUCCESS = 'certificates/PUSHCERT_SUCCESS';
export type PUSHCERT_FAILURE = 'certificates/PUSHCERT_FAILURE';
export const PUSHCERT_FAILURE: PUSHCERT_FAILURE = 'certificates/PUSHCERT_FAILURE';

export interface FetchPushCertificateAction {
    (): RSAA<PUSHCERT_REQUEST, PUSHCERT_SUCCESS, PUSHCERT_FAILURE>;
}

export const fetchPushCertificate: FetchPushCertificateAction = (): RSAA<PUSHCERT_REQUEST, PUSHCERT_SUCCESS, PUSHCERT_FAILURE> => {
    return {
        [CALL_API]: {
            endpoint: '/api/v1/push_certificate',
            method: 'GET',
            types: [
                PUSHCERT_REQUEST,
                PUSHCERT_SUCCESS,
                PUSHCERT_FAILURE
            ],
            headers: JSONAPI_HEADERS
        }
    }
};
