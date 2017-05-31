/// <reference path="../typings/redux-api-middleware.d.ts" />
import { CALL_API, RSAA } from 'redux-api-middleware';
import {JSONAPI_HEADERS, FlaskFilters, FlaskFilter} from './constants'
import {ThunkAction} from "redux-thunk";
import {RootState} from "../reducers/index";
import {
    RSAAIndexActionRequest, RSAAIndexActionResponse, encodeJSONAPIIndexParameters,
    RSAAReadActionRequest, RSAAReadActionResponse
} from "../constants";
import {Profile} from "../models";
import {JSONAPIDetailResponse} from "../json-api";
import {Dispatch} from "redux";


export type INDEX_REQUEST = 'profiles/INDEX_REQUEST';
export const INDEX_REQUEST: INDEX_REQUEST = 'profiles/INDEX_REQUEST';
export type INDEX_SUCCESS = 'profiles/INDEX_SUCCESS';
export const INDEX_SUCCESS: INDEX_SUCCESS = 'profiles/INDEX_SUCCESS';
export type INDEX_FAILURE = 'profiles/INDEX_FAILURE';
export const INDEX_FAILURE: INDEX_FAILURE = 'profiles/INDEX_FAILURE';

export type IndexActionRequest = RSAAIndexActionRequest<INDEX_REQUEST, INDEX_SUCCESS, INDEX_FAILURE>;
export type IndexActionResponse = RSAAIndexActionResponse<INDEX_REQUEST, INDEX_SUCCESS, INDEX_FAILURE, Profile>;

export const index = encodeJSONAPIIndexParameters((queryParameters: Array<String>) => {
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
});

export type READ_REQUEST = 'profiles/READ_REQUEST';
export const READ_REQUEST: READ_REQUEST = 'profiles/READ_REQUEST';
export type READ_SUCCESS = 'profiles/READ_SUCCESS';
export const READ_SUCCESS: READ_SUCCESS = 'profiles/READ_SUCCESS';
export type READ_FAILURE = 'profiles/READ_FAILURE';
export const READ_FAILURE: READ_FAILURE = 'profiles/READ_FAILURE';

export type ReadActionRequest = RSAAReadActionRequest<READ_REQUEST, READ_SUCCESS, READ_FAILURE>;
export type ReadActionResponse = RSAAReadActionResponse<READ_REQUEST, READ_SUCCESS, READ_FAILURE, JSONAPIDetailResponse<Profile, undefined>>;

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
export const setPage: ThunkAction<any, RootState, undefined> = (pageNumber: number) => (dispatch: Dispatch<RootState>, getState) => {
    
    // Dispatch index w page
};
