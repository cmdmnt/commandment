import {HTTPVerb, RSAA, RSAAction} from "redux-api-middleware";
import {
    encodeJSONAPIChildIndexParameters, encodeJSONAPIIndexParameters, JSONAPIListResponse, JSONAPIDataObject,
    RSAADeleteActionRequest,
    RSAADeleteActionResponse,
    RSAAIndexActionRequest,
    RSAAIndexActionResponse, RSAAPostActionRequest, RSAAPostActionResponse, RSAAReadActionRequest,
    RSAAReadActionResponse,
} from "../../json-api";
import {JSONAPIDetailResponse, JSONAPIErrorResponse, RSAAPatchActionRequest} from "../../json-api";
import {Application} from "./types";
import {FlaskFilter, FlaskFilters, JSON_HEADERS, JSONAPI_HEADERS} from "../constants";

export type INDEX_REQUEST = "applications/INDEX_REQUEST";
export const INDEX_REQUEST: INDEX_REQUEST = "applications/INDEX_REQUEST";
export type INDEX_SUCCESS = "applications/INDEX_SUCCESS";
export const INDEX_SUCCESS: INDEX_SUCCESS = "applications/INDEX_SUCCESS";
export type INDEX_FAILURE = "applications/INDEX_FAILURE";
export const INDEX_FAILURE: INDEX_FAILURE = "applications/INDEX_FAILURE";

export type IndexActionRequest = RSAAIndexActionRequest<INDEX_REQUEST, INDEX_SUCCESS, INDEX_FAILURE>;
export type IndexActionResponse = RSAAIndexActionResponse<INDEX_REQUEST, INDEX_SUCCESS, INDEX_FAILURE, Application>;

export const index = encodeJSONAPIIndexParameters((queryParameters: string[]) => {
    return ({
        [RSAA]: {
            endpoint: "/api/v1/applications?" + queryParameters.join("&"),
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

export const POST_REQUEST = "applications/POST_REQUEST";
export type POST_REQUEST = typeof POST_REQUEST;
export const POST_SUCCESS = "applications/POST_SUCCESS";
export type POST_SUCCESS = typeof POST_SUCCESS;
export const POST_FAILURE = "applications/POST_FAILURE";
export type POST_FAILURE = typeof POST_FAILURE;

export type PostActionRequest = RSAAPostActionRequest<POST_REQUEST, POST_SUCCESS, POST_FAILURE, Application>;
export type PostActionResponse = RSAAPostActionResponse<POST_REQUEST, POST_SUCCESS, POST_FAILURE, JSONAPIDetailResponse<Application, undefined>>;

export const post: PostActionRequest = (values: Application) => {
    return ({
        [RSAA]: {
            endpoint: `/api/v1/applications`,
            method: "POST",
            types: [
                POST_REQUEST,
                POST_SUCCESS,
                POST_FAILURE,
            ],
            headers: JSONAPI_HEADERS,
            body: JSON.stringify({
                data: {
                    attributes: values,
                    type: "applications",
                },
            }),
        },
    } as RSAAction<POST_REQUEST, POST_SUCCESS, POST_FAILURE>);
};

export type READ_REQUEST = "applications/READ_REQUEST";
export const READ_REQUEST: READ_REQUEST = "applications/READ_REQUEST";
export type READ_SUCCESS = "applications/READ_SUCCESS";
export const READ_SUCCESS: READ_SUCCESS = "applications/READ_SUCCESS";
export type READ_FAILURE = "applications/READ_FAILURE";
export const READ_FAILURE: READ_FAILURE = "applications/READ_FAILURE";

export type ReadActionRequest = RSAAReadActionRequest<READ_REQUEST, READ_SUCCESS, READ_FAILURE>;
export type ReadActionResponse = RSAAReadActionResponse<READ_REQUEST, READ_SUCCESS, READ_FAILURE, JSONAPIDetailResponse<Application, undefined>>;

export const read: ReadActionRequest = (id: string, include?: string[]) => {

    let inclusions = "";
    if (include && include.length) {
        inclusions = "include=" + include.join(",");
    }

    return {
        [RSAA]: {
            endpoint: `/api/v1/profiles/${id}?${inclusions}`,
            headers: JSONAPI_HEADERS,
            method: "GET",
            types: [
                READ_REQUEST,
                READ_SUCCESS,
                READ_FAILURE,
            ],
        },
    };
};

export const PATCH_REQUEST = "applications/PATCH_REQUEST";
export type PATCH_REQUEST = typeof PATCH_REQUEST;
export const PATCH_SUCCESS = "applications/PATCH_SUCCESS";
export type PATCH_SUCCESS = typeof PATCH_SUCCESS;
export const PATCH_FAILURE = "applications/PATCH_FAILURE";
export type PATCH_FAILURE = typeof PATCH_FAILURE;

export type PatchActionRequest = RSAAPatchActionRequest<PATCH_REQUEST, PATCH_SUCCESS, PATCH_FAILURE, Application>;
export type PatchActionResponse = RSAAReadActionResponse<PATCH_REQUEST, PATCH_SUCCESS, PATCH_FAILURE, JSONAPIDetailResponse<Application, undefined>>;

export const patch: PatchActionRequest = (applicationId: string, values: Application) => {

    return {
        [RSAA]: {
            body: JSON.stringify({
                data: {
                    attributes: values,
                    type: "applications",
                },
            }),
            endpoint: `/api/v1/applications/${applicationId}`,
            headers: JSONAPI_HEADERS,
            method: "PATCH",
            types: [
                PATCH_REQUEST,
                PATCH_SUCCESS,
                PATCH_FAILURE,
            ],
        },
    };
};

export type DELETE_REQUEST = "applications/DELETE_REQUEST";
export const DELETE_REQUEST: DELETE_REQUEST = "applications/DELETE_REQUEST";
export type DELETE_SUCCESS = "applications/DELETE_SUCCESS";
export const DELETE_SUCCESS: DELETE_SUCCESS = "applications/DELETE_SUCCESS";
export type DELETE_FAILURE = "applications/DELETE_FAILURE";
export const DELETE_FAILURE: DELETE_FAILURE = "applications/DELETE_FAILURE";

export const destroy: RSAADeleteActionRequest<DELETE_REQUEST, DELETE_SUCCESS, DELETE_FAILURE> = (id: string) => {
    return {
        [RSAA]: {
            endpoint: `/api/v1/applications/${id}`,
            headers: JSONAPI_HEADERS,
            method: "DELETE",
            types: [
                DELETE_REQUEST,
                DELETE_SUCCESS,
                DELETE_FAILURE,
            ],
        },
    };
};
