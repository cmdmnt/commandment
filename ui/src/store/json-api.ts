// Redux API Middleware Type Guards
import {ApiError, InvalidRSAA, RequestError, RSAAction} from "redux-api-middleware";
import {FlaskFilters} from "../flask-rest-jsonapi";
import {Action} from "redux";
import {Relationships} from "../json-api-v1";


export const JSONAPI_HEADERS = {
    "Accept": "application/vnd.api+json",
    "Content-Type": "application/vnd.api+json",
};

// http://jsonapi.org/format/#errors
export interface JSONAPIErrorObject {
    id?: any;
    links?: {
        about?: string;
    };
    status?: string;
    code?: string;
    title?: string;
    detail?: string;
    source?: {
        pointer?: string;
        parameter?: string;
    };
    meta?: any;
}

export interface JSONAPIErrorResponse {
    errors: JSONAPIErrorObject[];
    jsonapi: {
        version: string;
    };
}

export interface JSONAPIResourceIdentifier {
    type: string;
    id: string;
    meta?: {
        [index: string]: any;
    };
}

export type JSONAPILink = string | { href?: string, meta?: { [index: string]: any }};

export interface JSONAPILinks {
    self?: JSONAPILink;
    related?: JSONAPILink;

    // Pagination
    first?: JSONAPILink;
    last?: JSONAPILink;
    prev?: JSONAPILink;
    next?: JSONAPILink;
}

export interface JSONAPIRelationship {
    data: JSONAPIResourceIdentifier[] | JSONAPIResourceIdentifier | null,
    links?: JSONAPILinks;
}

export interface JSONAPIRelationships {
    [relationshipName: string]: JSONAPIRelationship;
}

export interface JSONAPIDataObject<TObject> {
    id: string|number;
    type: string;
    attributes: TObject;
    relationships?: JSONAPIRelationships;
    links?: JSONAPILinks;
}

export interface JSONAPIDataResponse<TData, TIncluded> {
    data?: TData;
    links?: JSONAPILinks;
    meta?: {
        count?: number;
    };
    jsonapi?: {
        version: string;
    };
}

export interface JSONAPIDetailResponse<TObject, TIncluded> {
    data?: JSONAPIDataObject<TObject>;
    included?: Array<JSONAPIDataObject<TIncluded>>;
    links?: JSONAPILinks;
    meta?: {
        count?: number;
    };
    jsonapi?: {
        version: string;
    };
}

export interface JSONAPIListResponse<TObject> {
    data?: TObject[];
    links?: JSONAPILinks;
    meta?: {
        count?: number;
    };
    jsonapi?: {
        version: string;
    };
}

export function isJSONAPIErrorResponsePayload(
    payload: JSONAPIListResponse<any> |
        JSONAPIDetailResponse<any, any> |
        JSONAPIErrorResponse): payload is JSONAPIErrorResponse {

    return (payload as JSONAPIErrorResponse).errors !== undefined;
}



// Standardised JSON-API Index ActionCreator
export type RSAAIndexActionRequest<TRequest, TSuccess, TFailure> =
    (size?: number, pageNumber?: number, sort?: string[], filters?: FlaskFilters) => RSAAction<TRequest, TSuccess, TFailure>;

// Standardised JSON-API Index ActionCreator Response (passed to reducer)

export interface RSAAResponseRequest<TRequest> extends Action<TRequest> {
    error?: boolean;
    payload?: InvalidRSAA | RequestError;
    type: TRequest;
}

export interface RSAAResponseFailure<TFailure> extends Action<TFailure> {
    payload: ApiError;
    type: TFailure;
}

// Success can still contain API errors that are 2xx responses
export interface RSAAResponseSuccess<TSuccess, TResponse> extends Action<TSuccess> {
    payload: TResponse;
    type: TSuccess;
}

export type RSAAIndexActionResponse<TRequest, TSuccess, TFailure, TObject> =
    RSAAResponseRequest<TRequest> |
    RSAAResponseFailure<TFailure> |
    RSAAResponseSuccess<TSuccess, JSONAPIListResponse<JSONAPIDataObject<TObject>>> |
    RSAAResponseSuccess<TSuccess, JSONAPIErrorResponse>;

// Standardised JSON-API Index ActionCreator that fetches a resource child of some object / by relationship
export type RSAAChildIndexActionRequest<TRequest, TSuccess, TFailure> =
    (parent_id: string, size?: number, pageNumber?: number, sort?: string[], filters?: FlaskFilters)
        => RSAAction<TRequest, TSuccess, TFailure>;

export type RSAAReadActionRequest<TRequest, TSuccess, TFailure> = (id: string, include?: string[])
    => RSAAction<TRequest, TSuccess, TFailure>;

export interface RSAAReadActionResponseSuccess<TSuccess, TResponse> {
    type: TSuccess;
    payload: TResponse;
}

export type RSAAReadActionResponse<TRequest, TSuccess, TFailure, TResponse> = RSAAResponseRequest<TRequest> |
    RSAAResponseFailure<TFailure> |
    RSAAReadActionResponseSuccess<TSuccess, TResponse> |
    RSAAReadActionResponseSuccess<TSuccess, JSONAPIErrorResponse>;

export type RSAAPostActionRequest<TRequest, TSuccess, TFailure, TValues> = (
    values: TValues, relationships?: Relationships)
    => RSAAction<TRequest, TSuccess, TFailure>;

export type RSAAPostActionResponse<TRequest, TSuccess, TFailure, TResponse> = RSAAResponseRequest<TRequest> |
    RSAAResponseFailure<TFailure> | RSAAResponseSuccess<TSuccess, TResponse | JSONAPIErrorResponse>;

export type RSAAPatchActionRequest<TRequest, TSuccess, TFailure, TValues> = (id: string, values: TValues)
    => RSAAction<TRequest, TSuccess, TFailure>;

export type RSAADeleteActionRequest<TRequest, TSuccess, TFailure> = (id: string) => RSAAction<TRequest, TSuccess, TFailure>;

export interface RSAADeleteActionResponseSuccess<TSuccess> {
    type: TSuccess;
}

export type RSAADeleteActionResponse<TRequest, TSuccess, TFailure, TResponse> = RSAAResponseRequest<TRequest> |
    RSAAResponseFailure<TFailure> | RSAADeleteActionResponseSuccess<TSuccess>;

