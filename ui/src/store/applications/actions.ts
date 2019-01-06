import {HTTPVerb, RSAA, RSAAction} from "redux-api-middleware";
import {
    encodeJSONAPIChildIndexParameters, encodeJSONAPIIndexParameters, JSONAPIListResponse, JSONAPIDataObject,
    RSAADeleteActionRequest,
    RSAADeleteActionResponse,
    RSAAIndexActionRequest,
    RSAAIndexActionResponse, RSAAPostActionRequest, RSAAPostActionResponse, RSAAReadActionRequest,
    RSAAReadActionResponse,
} from "../json-api";
import {JSONAPIDetailResponse, JSONAPIErrorResponse, RSAAPatchActionRequest} from "../json-api";
import {Application} from "./types";
import {FlaskFilter, FlaskFilters, JSON_HEADERS, JSONAPI_HEADERS} from "../constants";

export enum ApplicationsActionTypes {
    INDEX_REQUEST = "applications/INDEX_REQUEST",
    INDEX_SUCCESS = "applications/INDEX_SUCCESS",
    INDEX_FAILURE = "applications/INDEX_FAILURE",
    READ_REQUEST = "applications/READ_REQUEST",
    READ_SUCCESS = "applications/READ_SUCCESS",
    READ_FAILURE = "applications/READ_FAILURE",
    PATCH_REQUEST = "applications/PATCH_REQUEST",
    PATCH_SUCCESS = "applications/PATCH_SUCCESS",
    PATCH_FAILURE = "applications/PATCH_FAILURE",
}


export type IndexActionRequest = RSAAIndexActionRequest<ApplicationsActionTypes.INDEX_REQUEST, ApplicationsActionTypes.INDEX_SUCCESS, ApplicationsActionTypes.INDEX_FAILURE>;
export type IndexActionResponse = RSAAIndexActionResponse<ApplicationsActionTypes.INDEX_REQUEST, ApplicationsActionTypes.INDEX_SUCCESS, ApplicationsActionTypes.INDEX_FAILURE, Application>;

export const index = encodeJSONAPIIndexParameters((queryParameters: string[]) => {
    return ({
        [RSAA]: {
            endpoint: "/api/v1/applications?" + queryParameters.join("&"),
            headers: JSONAPI_HEADERS,
            method: ("GET" as HTTPVerb),
            types: [
                ApplicationsActionTypes.INDEX_REQUEST,
                ApplicationsActionTypes.INDEX_SUCCESS,
                ApplicationsActionTypes.INDEX_FAILURE,
            ],
        },
    } as RSAAction<ApplicationsActionTypes.INDEX_REQUEST, ApplicationsActionTypes.INDEX_SUCCESS, ApplicationsActionTypes.INDEX_FAILURE>);
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
            body: JSON.stringify({
                data: {
                    attributes: values,
                    type: "applications",
                },
            }),
            endpoint: `/api/v1/applications`,
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


export type ReadActionRequest = RSAAReadActionRequest<ApplicationsActionTypes.READ_REQUEST, ApplicationsActionTypes.READ_SUCCESS, ApplicationsActionTypes.READ_FAILURE>;
export type ReadActionResponse = RSAAReadActionResponse<ApplicationsActionTypes.READ_REQUEST, ApplicationsActionTypes.READ_SUCCESS, ApplicationsActionTypes.READ_FAILURE, JSONAPIDetailResponse<Application, undefined>>;

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
                ApplicationsActionTypes.READ_REQUEST,
                ApplicationsActionTypes.READ_SUCCESS,
                ApplicationsActionTypes.READ_FAILURE,
            ],
        },
    };
};

export type PatchActionRequest = RSAAPatchActionRequest<ApplicationsActionTypes.PATCH_REQUEST, ApplicationsActionTypes.PATCH_SUCCESS, ApplicationsActionTypes.PATCH_FAILURE, Application>;
export type PatchActionResponse = RSAAReadActionResponse<ApplicationsActionTypes.PATCH_REQUEST, ApplicationsActionTypes.PATCH_SUCCESS, ApplicationsActionTypes.PATCH_FAILURE, JSONAPIDetailResponse<Application, undefined>>;

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
                ApplicationsActionTypes.PATCH_REQUEST,
                ApplicationsActionTypes.PATCH_SUCCESS,
                ApplicationsActionTypes.PATCH_FAILURE,
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

export type ApplicationsActions = IndexActionResponse | PostActionResponse | PatchActionResponse;
