/// <reference path="../typings/redux-api-middleware.d.ts" />
import {Dispatch} from "react-redux";
import {ApiError, HTTPVerb, RSAA, RSAAction} from "redux-api-middleware";
import {ThunkAction} from "redux-thunk";
import {
    encodeJSONAPIIndexParameters, JSONAPIRelationship, RSAAIndexActionRequest,
    RSAAIndexActionResponse, RSAAReadActionRequest, RSAAReadActionResponse,
} from "../json-api";
import {JSONAPIDetailResponse} from "../json-api";
import {Profile, ProfileRelationship, Tag} from "../models";
import {IRootState} from "../reducers/index";
import {FlaskFilter, FlaskFilters, JSONAPI_HEADERS} from "./constants";

export type INDEX_REQUEST = "profiles/INDEX_REQUEST";
export const INDEX_REQUEST: INDEX_REQUEST = "profiles/INDEX_REQUEST";
export type INDEX_SUCCESS = "profiles/INDEX_SUCCESS";
export const INDEX_SUCCESS: INDEX_SUCCESS = "profiles/INDEX_SUCCESS";
export type INDEX_FAILURE = "profiles/INDEX_FAILURE";
export const INDEX_FAILURE: INDEX_FAILURE = "profiles/INDEX_FAILURE";

export type IndexActionRequest = RSAAIndexActionRequest<INDEX_REQUEST, INDEX_SUCCESS, INDEX_FAILURE>;
export type IndexActionResponse = RSAAIndexActionResponse<INDEX_REQUEST, INDEX_SUCCESS, INDEX_FAILURE, Profile>;

export const index = encodeJSONAPIIndexParameters((queryParameters: string[]) => {
    return ({
        [RSAA]: {
            endpoint: "/api/v1/profiles?" + encodeURI(queryParameters.join("&")),
            headers: JSONAPI_HEADERS,
            method: ("GET" as HTTPVerb),
            types: [
                INDEX_REQUEST,
                INDEX_SUCCESS,
                INDEX_FAILURE,
            ],
        },
    } as RSAAction<INDEX_REQUEST, INDEX_SUCCESS, INDEX_FAILURE>);
});

export type READ_REQUEST = "profiles/READ_REQUEST";
export const READ_REQUEST: READ_REQUEST = "profiles/READ_REQUEST";
export type READ_SUCCESS = "profiles/READ_SUCCESS";
export const READ_SUCCESS: READ_SUCCESS = "profiles/READ_SUCCESS";
export type READ_FAILURE = "profiles/READ_FAILURE";
export const READ_FAILURE: READ_FAILURE = "profiles/READ_FAILURE";

export type ReadActionRequest = RSAAReadActionRequest<READ_REQUEST, READ_SUCCESS, READ_FAILURE>;
export type ReadActionResponse = RSAAReadActionResponse<READ_REQUEST, READ_SUCCESS, READ_FAILURE, JSONAPIDetailResponse<Profile, undefined>>;

export const read: ReadActionRequest = (id: string, include?: string[]) => {

    let inclusions = "";
    if (include && include.length) {
        inclusions = "include=" + include.join(",");
    }

    return {
        [RSAA]: {
            endpoint: `/api/v1/profiles/${id}?${inclusions}`,
            method: "GET",
            types: [
                READ_REQUEST,
                READ_SUCCESS,
                READ_FAILURE,
            ],
            headers: JSONAPI_HEADERS,
        },
    };
};

export const RPATCH_REQUEST = "profiles/RPATCH_REQUEST";
export type RPATCH_REQUEST = typeof RPATCH_REQUEST;
export const RPATCH_SUCCESS = "profiles/RPATCH_SUCCESS";
export type RPATCH_SUCCESS = typeof RPATCH_SUCCESS;
export const RPATCH_FAILURE = "profiles/RPATCH_FAILURE";
export type RPATCH_FAILURE = typeof RPATCH_FAILURE;

type PatchRelationshipActionRequest = (parent_id: string, relationship: ProfileRelationship, data: JSONAPIRelationship[]) => RSAAction<RPATCH_REQUEST, RPATCH_SUCCESS, RPATCH_FAILURE>;
export type PatchRelationshipActionResponse = RSAAReadActionResponse<RPATCH_REQUEST, RPATCH_SUCCESS, RPATCH_FAILURE, JSONAPIDetailResponse<Profile, Tag>>;

export const patchRelationship: PatchRelationshipActionRequest = (id: string, relationship: ProfileRelationship, data: JSONAPIRelationship[]) => {
    return {
        [RSAA]: {
            endpoint: `/api/v1/profiles/${id}/relationships/${relationship}`,
            method: "PATCH",
            types: [
                RPATCH_REQUEST,
                RPATCH_SUCCESS,
                RPATCH_FAILURE,
            ],
            headers: JSONAPI_HEADERS,
            body: JSON.stringify({ data }),
        },
    };
};

export const UPLOAD = "profiles/UPLOAD";
export type UPLOAD = typeof UPLOAD;

export const UPLOAD_REQUEST = "profiles/UPLOAD_REQUEST";
export type UPLOAD_REQUEST = typeof UPLOAD_REQUEST;
export const UPLOAD_SUCCESS = "profiles/UPLOAD_SUCCESS";
export type UPLOAD_SUCCESS = typeof UPLOAD_SUCCESS;
export const UPLOAD_FAILURE = "profiles/UPLOAD_FAILURE";
export type UPLOAD_FAILURE = typeof UPLOAD_FAILURE;

type UploadActionRequest = (file: File) => ThunkAction<void, IRootState, void>;
export type UploadActionResponse = RSAAReadActionResponse<UPLOAD_REQUEST, UPLOAD_SUCCESS, UPLOAD_FAILURE, JSONAPIDetailResponse<Profile, undefined>>;

export const upload = (file: File): ThunkAction<void, IRootState, void> => (
    dispatch: Dispatch<IRootState>,
    getState: () => IRootState,
    extraArgument: void) => {

    const data = new FormData();
    data.append("file", file);
    dispatch({
        type: UPLOAD,
        payload: data,
    });

    dispatch({
        [RSAA]: {
            endpoint: `/api/v1/upload/profiles`,
            method: "POST",
            types: [
                UPLOAD_REQUEST,
                UPLOAD_SUCCESS,
                UPLOAD_FAILURE,
            ],
            body: data,
        },
    });
};
