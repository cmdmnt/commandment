/// <reference path="../typings/redux-api-middleware.d.ts" />
import { CALL_API, RSAA } from 'redux-api-middleware';
import {JSONAPI_HEADERS, FlaskFilters, FlaskFilter} from './constants'
import {
    RSAAIndexActionRequest, RSAAIndexActionResponse, encodeJSONAPIIndexParameters,
    RSAAReadActionRequest, RSAAReadActionResponse, JSONAPIRelationship
} from "../json-api";
import {Profile, ProfileRelationship, Tag} from "../models";
import {JSONAPIDetailResponse} from "../json-api";



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

export const read: ReadActionRequest = (id: string, include?: Array<string>) => {

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


export const RPATCH_REQUEST = 'profiles/RPATCH_REQUEST';
export type RPATCH_REQUEST = typeof RPATCH_REQUEST;
export const RPATCH_SUCCESS = 'profiles/RPATCH_SUCCESS';
export type RPATCH_SUCCESS = typeof RPATCH_SUCCESS;
export const RPATCH_FAILURE = 'profiles/RPATCH_FAILURE';
export type RPATCH_FAILURE = typeof RPATCH_FAILURE;

export interface PatchRelationshipActionRequest {
    (parent_id: string, relationship: ProfileRelationship, data: Array<JSONAPIRelationship>): RSAA<RPATCH_REQUEST, RPATCH_SUCCESS, RPATCH_FAILURE>;
}
export type PatchRelationshipActionResponse = RSAAReadActionResponse<RPATCH_REQUEST, RPATCH_SUCCESS, RPATCH_FAILURE, JSONAPIDetailResponse<Profile, Tag>>;

export const patchRelationship: PatchRelationshipActionRequest = (id: string, relationship: ProfileRelationship, data: Array<JSONAPIRelationship>) => {
    return {
        [CALL_API]: {
            endpoint: `/api/v1/profiles/${id}/relationships/${relationship}`,
            method: 'PATCH',
            types: [
                RPATCH_REQUEST,
                RPATCH_SUCCESS,
                RPATCH_FAILURE
            ],
            headers: JSONAPI_HEADERS,
            body: JSON.stringify({ data })
        }
    }
};

