import {Dispatch} from "redux";
import {HTTPVerb, RSAA, RSAAction} from "redux-api-middleware";
import {ThunkAction} from "redux-thunk";
import {
    JSONAPIDataObject, JSONAPIListResponse,
    RSAAIndexActionRequest,
    RSAAIndexActionResponse, RSAAPostActionRequest, RSAAPostActionResponse, RSAAReadActionRequest,
    RSAAReadActionResponse,
} from "../json-api";
import {JSONAPIDetailResponse, JSONAPIErrorResponse} from "../json-api";
import {RootState} from "../../reducers/index";
import {JSON_HEADERS, JSONAPI_HEADERS} from "../constants"
import {Tag} from "./types";
import {
    encodeJSONAPIChildIndexParameters,
    encodeJSONAPIIndexParameters,
    FlaskFilter,
    FlaskFilters
} from "../../flask-rest-jsonapi";

export enum TagsActionTypes {
    INDEX_REQUEST = "tags/INDEX_REQUEST",
    INDEX_SUCCESS = "tags/INDEX_SUCCESS",
    INDEX_FAILURE = "tags/INDEX_FAILURE",

    POST_REQUEST = "tags/POST_REQUEST",
    POST_SUCCESS = "tags/POST_SUCCESS",
    POST_FAILURE = "tags/POST_FAILURE",
}

export type IndexActionRequest = RSAAIndexActionRequest<TagsActionTypes.INDEX_REQUEST, TagsActionTypes.INDEX_SUCCESS, TagsActionTypes.INDEX_FAILURE>;
export type IndexActionResponse = RSAAIndexActionResponse<TagsActionTypes.INDEX_REQUEST, TagsActionTypes.INDEX_SUCCESS, TagsActionTypes.INDEX_FAILURE, Tag>;

export const index = encodeJSONAPIIndexParameters((queryParameters: string[]) => {
    return ({
        [RSAA]: {
            endpoint: "/api/v1/tags?" + queryParameters.join("&"),
            headers: JSONAPI_HEADERS,
            method: ("GET" as HTTPVerb),
            types: [
                TagsActionTypes.INDEX_REQUEST,
                TagsActionTypes.INDEX_SUCCESS,
                TagsActionTypes.INDEX_FAILURE,
            ],
        },
    } as RSAAction<TagsActionTypes.INDEX_REQUEST, TagsActionTypes.INDEX_SUCCESS, TagsActionTypes.INDEX_FAILURE>);
});

export type PostActionRequest = RSAAPostActionRequest<TagsActionTypes.POST_REQUEST, TagsActionTypes.POST_SUCCESS, TagsActionTypes.POST_FAILURE, Tag>;
export type PostActionResponse = RSAAPostActionResponse<TagsActionTypes.POST_REQUEST, TagsActionTypes.POST_SUCCESS, TagsActionTypes.POST_FAILURE, JSONAPIDetailResponse<Tag, undefined>>;

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
                TagsActionTypes.POST_REQUEST,
                TagsActionTypes.POST_SUCCESS,
                TagsActionTypes.POST_FAILURE,
            ],
        },
    } as RSAAction<TagsActionTypes.POST_REQUEST, TagsActionTypes.POST_SUCCESS, TagsActionTypes.POST_FAILURE>);
};

export type CreateAndApplyRequest = (values: Tag) => ThunkAction<void, RootState, void, PostActionResponse>;

export const createAndApply: CreateAndApplyRequest = (values) => (dispatch: Dispatch, getState) => {
    dispatch(post(values));
};
