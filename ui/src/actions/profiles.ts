/// <reference path="../typings/redux-api-middleware.d.ts" />
import { CALL_API, RSAA } from 'redux-api-middleware';
import {JSONAPI_HEADERS, FlaskFilters, FlaskFilter} from './constants'
import {ThunkAction} from "redux-thunk";
import {RootState} from "../reducers/index";

export type INDEX_REQUEST = 'profiles/INDEX_REQUEST';
export const INDEX_REQUEST: INDEX_REQUEST = 'profiles/INDEX_REQUEST';
export type INDEX_SUCCESS = 'profiles/INDEX_SUCCESS';
export const INDEX_SUCCESS: INDEX_SUCCESS = 'profiles/INDEX_SUCCESS';
export type INDEX_FAILURE = 'profiles/INDEX_FAILURE';
export const INDEX_FAILURE: INDEX_FAILURE = 'profiles/INDEX_FAILURE';

export interface IndexActionRequest {
    (size?: number, number?: number, sort?: Array<string>, filter?: Array<FlaskFilter>): RSAA<INDEX_REQUEST, INDEX_SUCCESS, INDEX_FAILURE>;
}

export interface IndexActionResponse {
    type: INDEX_REQUEST | INDEX_FAILURE | INDEX_SUCCESS;
    payload?: JSONAPIListResponse<JSONAPIObject<Profile>> | JSONAPIErrorResponse;
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
            endpoint: '/api/v1/profiles?' + queryParameters.join('&'),
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


export type READ_REQUEST = 'profiles/READ_REQUEST';
export const READ_REQUEST: READ_REQUEST = 'profiles/READ_REQUEST';
export type READ_SUCCESS = 'profiles/READ_SUCCESS';
export const READ_SUCCESS: READ_SUCCESS = 'profiles/READ_SUCCESS';
export type READ_FAILURE = 'profiles/READ_FAILURE';
export const READ_FAILURE: READ_FAILURE = 'profiles/READ_FAILURE';

export interface ReadActionRequest {
    (id: number, include?: Array<string>): RSAA<READ_REQUEST, READ_SUCCESS, READ_FAILURE>;
}

export interface ReadActionResponse {
    type: READ_REQUEST | READ_FAILURE | READ_SUCCESS;
    payload?: JSONAPIDetailResponse<Profile, undefined> | JSONAPIErrorResponse;
}

export const read: ReadActionRequest = (id: number, include?: Array<string>) => {

    let inclusions = '';
    if (include && include.length) {
        inclusions = 'include=' + include.join(',')
    }

    return {
        [CALL_API]: {
            endpoint: `/api/v1/profiles/${id}?${inclusions}`,
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

export type NEXT_PAGE = 'profiles/NEXT_PAGE';
export const NEXT_PAGE: NEXT_PAGE = 'profiles/NEXT_PAGE';
export const nextPage = () => {
    return {
        type: NEXT_PAGE
    };
};

export type PREV_PAGE = 'profiles/PREV_PAGE';
export const PREV_PAGE: PREV_PAGE = 'profiles/PREV_PAGE';
export const prevPage = () => {
    return {
        type: PREV_PAGE
    };
};

export type SET_PAGE = 'profiles/SET_PAGE';
export const SET_PAGE: SET_PAGE = 'profiles/SET_PAGE';
export const setPage: ThunkAction<any, RootState, undefined> = (pageNumber: number) => (dispatch, getState) => {
    
    // Dispatch index w page
};
