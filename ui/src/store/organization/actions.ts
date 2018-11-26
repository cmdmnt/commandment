/// <reference path="../typings/redux-api-middleware.d.ts" />
import { RSAA, RSAAction } from "redux-api-middleware";
import {RSAAReadActionRequest, RSAAReadActionResponse} from "../../json-api";
import {JSON_HEADERS, JSONAPI_HEADERS} from "../constants"
import {Organization} from "./types";

export type READ_REQUEST = "organization/READ_REQUEST";
export const READ_REQUEST: READ_REQUEST = "organization/READ_REQUEST";
export type READ_SUCCESS = "organization/READ_SUCCESS";
export const READ_SUCCESS: READ_SUCCESS = "organization/READ_SUCCESS";
export type READ_FAILURE = "organization/READ_FAILURE";
export const READ_FAILURE: READ_FAILURE = "organization/READ_FAILURE";

type ReadActionRequest = () => RSAAction<READ_REQUEST, READ_SUCCESS, READ_FAILURE>;

export type ReadActionResponse = RSAAReadActionResponse<READ_REQUEST, READ_SUCCESS, READ_FAILURE, Organization>;

export const read: ReadActionRequest = () => {
    return {
        [RSAA]: {
            endpoint: "/api/v1/configuration/organization",
            headers: JSON_HEADERS,
            method: "GET",
            types: [
                READ_REQUEST,
                READ_SUCCESS,
                READ_FAILURE,
            ],
        },
    }
};

export type POST_REQUEST = "organization/POST_REQUEST";
export const POST_REQUEST: POST_REQUEST = "organization/POST_REQUEST";
export type POST_SUCCESS = "organization/POST_SUCCESS";
export const POST_SUCCESS: POST_SUCCESS = "organization/POST_SUCCESS";
export type POST_FAILURE = "organization/POST_FAILURE";
export const POST_FAILURE: POST_FAILURE = "organization/POST_FAILURE";

type PostActionRequest = (values: Organization) => RSAAction<POST_REQUEST, POST_SUCCESS, POST_FAILURE>;

export interface PostActionResponse {
    type: POST_REQUEST | POST_FAILURE | POST_SUCCESS;
    payload?: Organization;
}

export const post: PostActionRequest = (values: Organization) => {
    return {
        [RSAA]: {
            body: JSON.stringify(values),
            endpoint: "/api/v1/configuration/organization",
            headers: JSON_HEADERS,
            method: "POST",
            types: [
                POST_REQUEST,
                POST_SUCCESS,
                POST_FAILURE,
            ],
        },
    }
};
