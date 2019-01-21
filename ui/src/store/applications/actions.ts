import * as fetchJsonp from "fetch-jsonp";
import {Action} from "redux";
import {HTTPVerb, RSAA, RSAAction} from "redux-api-middleware";
import {ThunkAction} from "redux-thunk";
import {RootState} from "../../reducers";
import {JSON_HEADERS, JSONAPI_HEADERS} from "../constants";
import {JSONAPIDetailResponse, JSONAPIErrorResponse, RSAAPatchActionRequest} from "../json-api";
import {
    JSONAPIRelationship,
    JSONAPIRelationships, RSAAChildIndexActionRequest,
    RSAADeleteActionRequest,
    RSAADeleteActionResponse,
    RSAAIndexActionRequest,
    RSAAIndexActionResponse,
    RSAAPostActionRequest,
    RSAAPostActionResponse,
    RSAAReadActionRequest,
    RSAAReadActionResponse,
} from "../json-api";
import {EntityType, IItunesSearchQuery, IiTunesSearchResult, MediaType} from "./itunes";
import {ManagedApplicationsActionTypes} from "./managed";
import {
    Application,
    ApplicationRelationship,
    IOSStoreApplication,
    MacStoreApplication,
    ManagedApplication,
} from "./types";
import {
    encodeJSONAPIChildIndexParameters,
    encodeJSONAPIIndexParameters,
    FlaskFilter,
    FlaskFilters
} from "../../flask-rest-jsonapi";
import {RelationshipData} from "../../json-api-v1";

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

    REL_PATCH_REQUEST = "applications/relationships/PATCH_REQUEST",
    REL_PATCH_SUCCESS = "applications/relationships/PATCH_SUCCESS",
    REL_PATCH_FAILURE = "applications/relationships/PATCH_FAILURE",
    REL_DELETE_REQUEST = "applications/relationships/DELETE_REQUEST",
    REL_DELETE_SUCCESS = "applications/relationships/DELETE_SUCCESS",
    REL_DELETE_FAILURE = "applications/relationships/DELETE_FAILURE",

    MANAGED_REQUEST = "applications/MANAGED_REQUEST",
    MANAGED_SUCCESS = "applications/MANAGED_SUCCESS",
    MANAGED_FAILURE = "applications/MANAGED_FAILURE",

    ITUNES_SEARCH_REQUEST = "applications/ITUNES_SEARCH_REQUEST",
    ITUNES_SEARCH_SUCCESS = "applications/ITUNES_SEARCH_SUCCESS",
    ITUNES_SEARCH_FAILURE = "applications/ITUNES_SEARCH_FAILURE",
}

export type ManagedActionRequest = RSAAChildIndexActionRequest<
    ApplicationsActionTypes.MANAGED_REQUEST,
    ApplicationsActionTypes.MANAGED_SUCCESS,
    ApplicationsActionTypes.MANAGED_FAILURE>;
export type ManagedActionResponse = RSAAIndexActionResponse<
    ApplicationsActionTypes.MANAGED_REQUEST,
    ApplicationsActionTypes.MANAGED_SUCCESS,
    ApplicationsActionTypes.MANAGED_FAILURE,
    ManagedApplication>;

export const managed = encodeJSONAPIChildIndexParameters((appId: string, queryParameters: string[])  => {
    return ({
        [RSAA]: {
            endpoint: `/api/v1/applications/${appId}/managed_applications?${queryParameters.join("&")}`,
            headers: JSONAPI_HEADERS,
            method: "GET",
            types: [
                ApplicationsActionTypes.MANAGED_REQUEST,
                ApplicationsActionTypes.MANAGED_SUCCESS,
                ApplicationsActionTypes.MANAGED_FAILURE,
            ],
        },
    } as RSAAction<
        ApplicationsActionTypes.MANAGED_REQUEST,
        ApplicationsActionTypes.MANAGED_SUCCESS,
        ApplicationsActionTypes.MANAGED_FAILURE>);
});

export type IndexActionRequest = RSAAIndexActionRequest<
    ApplicationsActionTypes.INDEX_REQUEST,
    ApplicationsActionTypes.INDEX_SUCCESS,
    ApplicationsActionTypes.INDEX_FAILURE>;
export type IndexActionResponse = RSAAIndexActionResponse<
    ApplicationsActionTypes.INDEX_REQUEST,
    ApplicationsActionTypes.INDEX_SUCCESS,
    ApplicationsActionTypes.INDEX_FAILURE,
    Application>;

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
    } as RSAAction<
        ApplicationsActionTypes.INDEX_REQUEST,
        ApplicationsActionTypes.INDEX_SUCCESS,
        ApplicationsActionTypes.INDEX_FAILURE>);
});

export type PostActionRequest = RSAAPostActionRequest<
    ApplicationsActionTypes.POST_REQUEST,
    ApplicationsActionTypes.POST_SUCCESS,
    ApplicationsActionTypes.POST_FAILURE,
    Application>;
export type PostActionResponse = RSAAPostActionResponse<
    ApplicationsActionTypes.POST_REQUEST,
    ApplicationsActionTypes.POST_SUCCESS,
    ApplicationsActionTypes.POST_FAILURE,
    JSONAPIDetailResponse<Application, undefined>>;

export const post: PostActionRequest = (values: Application, relationships: RelationshipData) => {
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

export const postAppStoreMac: PostActionRequest = (values: MacStoreApplication, relationships: JSONAPIRelationships) => {
    return ({
        [RSAA]: {
            body: JSON.stringify({
                data: {
                    attributes: values,
                    type: "applications",
                },
            }),
            endpoint: `/api/v1/applications/store/mac`,
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

export const postAppStoreIos: PostActionRequest = (values: IOSStoreApplication, relationships: JSONAPIRelationships) => {
    return ({
        [RSAA]: {
            body: JSON.stringify({
                data: {
                    attributes: values,
                    type: "applications",
                },
            }),
            endpoint: `/api/v1/applications/store/ios`,
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

export type ReadActionRequest = RSAAReadActionRequest<
    ApplicationsActionTypes.READ_REQUEST,
    ApplicationsActionTypes.READ_SUCCESS,
    ApplicationsActionTypes.READ_FAILURE>;
export type ReadActionResponse = RSAAReadActionResponse<
    ApplicationsActionTypes.READ_REQUEST,
    ApplicationsActionTypes.READ_SUCCESS,
    ApplicationsActionTypes.READ_FAILURE,
    JSONAPIDetailResponse<Application, undefined>>;

export const read: ReadActionRequest = (id: string, include?: string[]) => {

    let inclusions = "";
    if (include && include.length) {
        inclusions = "include=" + include.join(",");
    }

    return {
        [RSAA]: {
            endpoint: `/api/v1/applications/${id}?${inclusions}`,
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

export type PatchActionRequest = RSAAPatchActionRequest<
    ApplicationsActionTypes.PATCH_REQUEST,
    ApplicationsActionTypes.PATCH_SUCCESS,
    ApplicationsActionTypes.PATCH_FAILURE,
    Application>;
export type PatchActionResponse = RSAAReadActionResponse<
    ApplicationsActionTypes.PATCH_REQUEST,
    ApplicationsActionTypes.PATCH_SUCCESS,
    ApplicationsActionTypes.PATCH_FAILURE,
    JSONAPIDetailResponse<Application, undefined>>;

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

export type DeleteActionRequest = RSAADeleteActionRequest<
    ApplicationsActionTypes.DELETE_REQUEST,
    ApplicationsActionTypes.DELETE_SUCCESS,
    ApplicationsActionTypes.DELETE_FAILURE>;
export type DeleteActionResponse = RSAADeleteActionResponse<
    ApplicationsActionTypes.DELETE_REQUEST,
    ApplicationsActionTypes.DELETE_SUCCESS,
    ApplicationsActionTypes.DELETE_FAILURE,
    Application>;

export const destroy: DeleteActionRequest = (id: string) => {
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

export type PatchRelationshipActionRequest = (
    applicationId: string,
    relationship: ApplicationRelationship,
    data: JSONAPIRelationship[],
) => RSAAction<
    ApplicationsActionTypes.REL_PATCH_REQUEST,
    ApplicationsActionTypes.REL_PATCH_SUCCESS,
    ApplicationsActionTypes.REL_PATCH_FAILURE>;

export type PatchRelationshipActionResponse = RSAAReadActionResponse<
    ApplicationsActionTypes.REL_PATCH_REQUEST,
    ApplicationsActionTypes.REL_PATCH_SUCCESS,
    ApplicationsActionTypes.REL_PATCH_FAILURE,
    JSONAPIDetailResponse<Application, undefined>>;

export const patchRelationship: PatchRelationshipActionRequest = (
    applicationId: string, relationship: ApplicationRelationship, data: JSONAPIRelationship[]) => {
    return {
        [RSAA]: {
            body: JSON.stringify({ data }),
            endpoint: `/api/v1/applications/${applicationId}/relationships/${relationship}`,
            headers: JSONAPI_HEADERS,
            method: "PATCH",
            types: [
                ApplicationsActionTypes.REL_PATCH_REQUEST,
                ApplicationsActionTypes.REL_PATCH_SUCCESS,
                ApplicationsActionTypes.REL_PATCH_FAILURE,
            ],
        },
    }
};

export type DeleteRelationshipActionRequest = (
    applicationId: string,
    relationship: ApplicationRelationship,
    data: JSONAPIRelationship[],
) => RSAAction<
    ApplicationsActionTypes.REL_DELETE_REQUEST,
    ApplicationsActionTypes.REL_DELETE_SUCCESS,
    ApplicationsActionTypes.REL_DELETE_FAILURE>;

export type DeleteRelationshipActionResponse = RSAAReadActionResponse<
    ApplicationsActionTypes.REL_DELETE_REQUEST,
    ApplicationsActionTypes.REL_DELETE_SUCCESS,
    ApplicationsActionTypes.REL_DELETE_FAILURE,
    JSONAPIDetailResponse<Application, undefined>>;

export const deleteRelationship: DeleteRelationshipActionRequest = (
    applicationId: string, relationship: ApplicationRelationship, data: JSONAPIRelationship[]) => {
    return {
        [RSAA]: {
            body: JSON.stringify({ data }),
            endpoint: `/api/v1/applications/${applicationId}/relationships/${relationship}`,
            headers: JSONAPI_HEADERS,
            method: "DELETE",
            types: [
                ApplicationsActionTypes.REL_DELETE_REQUEST,
                ApplicationsActionTypes.REL_DELETE_SUCCESS,
                ApplicationsActionTypes.REL_DELETE_FAILURE,
            ],
        },
    }
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

export type ApplicationsActions = IndexActionResponse | PostActionResponse | PatchActionResponse |
    ReadActionResponse | PatchRelationshipActionResponse | DeleteRelationshipActionResponse | ItunesSearchActions;
