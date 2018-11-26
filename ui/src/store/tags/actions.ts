/// <reference path="../../typings/redux-api-middleware.d.ts" />
import {Dispatch} from "redux";
import {HTTPVerb, RSAA, RSAAction} from "redux-api-middleware";
import {ThunkAction} from "redux-thunk";
import {
    encodeJSONAPIChildIndexParameters, encodeJSONAPIIndexParameters, JSONAPIDataObject, JSONAPIListResponse,
    RSAAIndexActionRequest,
    RSAAIndexActionResponse, RSAAPostActionRequest, RSAAPostActionResponse, RSAAReadActionRequest,
    RSAAReadActionResponse,
} from "../../json-api";
import {JSONAPIDetailResponse, JSONAPIErrorResponse} from "../../json-api";
import {Tag} from "../../models";
import {RootState} from "../../reducers/index";
import {FlaskFilter, FlaskFilters, JSON_HEADERS, JSONAPI_HEADERS} from "../../actions/constants"

export type INDEX_REQUEST = "tags/INDEX_REQUEST";
export const INDEX_REQUEST: INDEX_REQUEST = "tags/INDEX_REQUEST";
export type INDEX_SUCCESS = "tags/INDEX_SUCCESS";
export const INDEX_SUCCESS: INDEX_SUCCESS = "tags/INDEX_SUCCESS";
export type INDEX_FAILURE = "tags/INDEX_FAILURE";
export const INDEX_FAILURE: INDEX_FAILURE = "tags/INDEX_FAILURE";

export type IndexActionRequest = RSAAIndexActionRequest<INDEX_REQUEST, INDEX_SUCCESS, INDEX_FAILURE>;
export type IndexActionResponse = RSAAIndexActionResponse<INDEX_REQUEST, INDEX_SUCCESS, INDEX_FAILURE, Tag>;

export const index = encodeJSONAPIIndexParameters((queryParameters: String[]) => {
    return ({
        [RSAA]: {
            endpoint: "/api/v1/tags?" + queryParameters.join("&"),
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

export const POST_REQUEST = "tags/POST_REQUEST";
export type POST_REQUEST = typeof POST_REQUEST;
export const POST_SUCCESS = "tags/POST_SUCCESS";
export type POST_SUCCESS = typeof POST_SUCCESS;
export const POST_FAILURE = "tags/POST_FAILURE";
export type POST_FAILURE = typeof POST_FAILURE;

export type PostActionRequest = RSAAPostActionRequest<POST_REQUEST, POST_SUCCESS, POST_FAILURE, Tag>;
export type PostActionResponse = RSAAPostActionResponse<POST_REQUEST, POST_SUCCESS, POST_FAILURE, JSONAPIDetailResponse<Tag, undefined>>;

export const post: PostActionRequest = (values: Tag) => {

    return ({
        [RSAA]: {
            body: JSON.stringify({
                data: {
                    attributes: values,
                    type: "tags",
                },
            }),
            endpoint: `/api/v1/tags`,
            headers: JSONAPI_HEADERS,
            method: "POST",
            types: [
                POST_REQUEST,
                POST_SUCCESS,
                POST_FAILURE,
            ],
        },
    } as RSAAction<POST_REQUEST, POST_SUCCESS, POST_FAILURE>);
};

export type CreateAndApplyRequest = (values: Tag) => ThunkAction<void, RootState, void>;

export const createAndApply: CreateAndApplyRequest = (values) => (dispatch, getState) => {
    dispatch(post(values));

};
