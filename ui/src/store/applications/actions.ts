import {HTTPVerb, RSAA, RSAAction} from "redux-api-middleware";
import * as fetchJsonp from "fetch-jsonp";
import {FlaskFilter, FlaskFilters, JSON_HEADERS, JSONAPI_HEADERS} from "../constants";
import {
    encodeJSONAPIChildIndexParameters, encodeJSONAPIIndexParameters, JSONAPIDataObject, JSONAPIListResponse,
    RSAADeleteActionRequest,
    RSAADeleteActionResponse,
    RSAAIndexActionRequest,
    RSAAIndexActionResponse, RSAAPostActionRequest, RSAAPostActionResponse, RSAAReadActionRequest,
    RSAAReadActionResponse,
} from "../json-api";
import {JSONAPIDetailResponse, JSONAPIErrorResponse, RSAAPatchActionRequest} from "../json-api";
import {Application} from "./types";
import {ThunkAction} from "redux-thunk";
import {RootState} from "../../reducers";
import {EntityType, IItunesSearchQuery, IiTunesSearchResult, MediaType} from "./itunes";
import {Action} from "redux";

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
    POST_REQUEST = "applications/POST_REQUEST",
    POST_SUCCESS = "applications/POST_SUCCESS",
    POST_FAILURE = "applications/POST_FAILURE",
    DELETE_REQUEST = "applications/DELETE_REQUEST",
    DELETE_SUCCESS = "applications/DELETE_SUCCESS",
    DELETE_FAILURE = "applications/DELETE_FAILURE",

    ITUNES_SEARCH_REQUEST = "applications/ITUNES_SEARCH_REQUEST",
    ITUNES_SEARCH_SUCCESS = "applications/ITUNES_SEARCH_SUCCESS",
    ITUNES_SEARCH_FAILURE = "applications/ITUNES_SEARCH_FAILURE",
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

export type PostActionRequest = RSAAPostActionRequest<ApplicationsActionTypes.POST_REQUEST, ApplicationsActionTypes.POST_SUCCESS, ApplicationsActionTypes.POST_FAILURE, Application>;
export type PostActionResponse = RSAAPostActionResponse<ApplicationsActionTypes.POST_REQUEST, ApplicationsActionTypes.POST_SUCCESS, ApplicationsActionTypes.POST_FAILURE, JSONAPIDetailResponse<Application, undefined>>;

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
                ApplicationsActionTypes.POST_REQUEST,
                ApplicationsActionTypes.POST_SUCCESS,
                ApplicationsActionTypes.POST_FAILURE,
            ],
        },
    } as RSAAction<
        ApplicationsActionTypes.POST_REQUEST,
        ApplicationsActionTypes.POST_SUCCESS,
        ApplicationsActionTypes.POST_FAILURE>);
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

export const destroy: RSAADeleteActionRequest<ApplicationsActionTypes.DELETE_REQUEST, ApplicationsActionTypes.DELETE_SUCCESS, ApplicationsActionTypes.DELETE_FAILURE> = (id: string) => {
    return {
        [RSAA]: {
            endpoint: `/api/v1/applications/${id}`,
            headers: JSONAPI_HEADERS,
            method: "DELETE",
            types: [
                ApplicationsActionTypes.DELETE_REQUEST,
                ApplicationsActionTypes.DELETE_SUCCESS,
                ApplicationsActionTypes.DELETE_FAILURE,
            ],
        },
    };
};

export interface ITunesSearchRequestAction extends Action<ApplicationsActionTypes.ITUNES_SEARCH_REQUEST> {
    payload: IItunesSearchQuery;
}

export interface ITunesSearchSuccessAction extends Action<ApplicationsActionTypes.ITUNES_SEARCH_SUCCESS> {
    payload: IiTunesSearchResult;
}

export interface ITunesSearchFailureAction extends Action<ApplicationsActionTypes.ITUNES_SEARCH_FAILURE> {
    error: boolean;
    errorDetail: any;
}

export type ItunesSearchActions = ITunesSearchRequestAction | ITunesSearchSuccessAction | ITunesSearchFailureAction;


export type ItunesSearchAction = (
    term: string,
    country: string,
    media: MediaType,
    entity: EntityType,
    limit?: number) => ThunkAction<void, RootState, void, ItunesSearchActions>;

export const itunesSearch: ItunesSearchAction = (
    term: string,
    country: string,
    media: MediaType,
    entity: EntityType,
    limit?: number) => (dispatch, getState) => {

    dispatch({
        payload: { term, country, media, entity, limit },
        type: ApplicationsActionTypes.ITUNES_SEARCH_REQUEST,
    });

    const query = `term=${term}&country=${country}&entity=${entity}`;

    fetchJsonp(`https://itunes.apple.com/search?${query}`).then((response) => {
        return response.json();
    }).then((json) => {
        dispatch({
            payload: json,
            type: ApplicationsActionTypes.ITUNES_SEARCH_SUCCESS,
        });
    }).catch((e) => {
        dispatch({
            error: true,
            errorDetail: e,
            type: ApplicationsActionTypes.ITUNES_SEARCH_FAILURE,
        })
    });
};

export type ApplicationsActions = IndexActionResponse | PostActionResponse | PatchActionResponse | ItunesSearchActions;
