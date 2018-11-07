// Redux API Middleware Type Guards
import {FlaskFilters} from "./actions/constants";
import {ApiError, InvalidRSAA, RequestError, RSAAction} from "redux-api-middleware";

export const JSONAPI_HEADERS = {
    'Content-Type': 'application/vnd.api+json',
    'Accept': 'application/vnd.api+json'
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
    errors: Array<JSONAPIErrorObject>;
    jsonapi: {
        version: string;
    }
}

export interface JSONAPIRelationship {
    type: string;
    id: string;
}

export interface JSONAPIRelationships {
    [relationshipName: string]: {
        data: Array<JSONAPIRelationship> | JSONAPIRelationship,
        links?: {
            related?: string;
        }
    }
}

export interface JSONAPIObject<TObject> {
    id: string|number;
    type: string;
    attributes: TObject;
    relationships?: JSONAPIRelationships;
    links?: {
        self?: string;
    }
}

export interface JSONAPIDetailResponse<TObject, TIncluded> {
    data?: JSONAPIObject<TObject>;
    included?: Array<JSONAPIObject<TIncluded>>;
    links?: {
        self?: string;
    },
    meta?: {
        count?: number;
    }
    jsonapi: {
        version: string;
    }
}

export interface JSONAPIListResponse<TObject> {
    data?: Array<TObject>;
    links?: {
        self?: string;
    },
    meta?: {
        count?: number;
    }
    jsonapi: {
        version: string;
    }
}

export function isJSONAPIErrorResponsePayload(
    payload: JSONAPIListResponse<any> |
        JSONAPIDetailResponse<any, any> |
        JSONAPIErrorResponse): payload is JSONAPIErrorResponse {

    return (<JSONAPIErrorResponse>payload).errors !== undefined;
}


interface WrappedChildIndexActionCreator<R> {
    (id: string, queryParameters: Array<String>): R;
}

interface WrappedIndexActionCreator<R> {
    (queryParameters: Array<String>): R;
}

// Standardised JSON-API Index ActionCreator
export interface RSAAIndexActionRequest<TRequest, TSuccess, TFailure> {
    (size?: number, pageNumber?: number, sort?: Array<string>, filters?: FlaskFilters): RSAAction<TRequest, TSuccess, TFailure>;
}

// Standardised JSON-API Index ActionCreator Response (passed to reducer)

export interface RSAAResponseRequest<TRequest> {
    type: TRequest;
    payload?: InvalidRSAA | RequestError;
    error?: boolean;
}

export interface RSAAResponseFailure<TFailure> {
    type: TFailure;
    payload: ApiError;
}

// Success can still contain API errors that are 2xx responses
export interface RSAAResponseSuccess<TSuccess, TResponse> {
    type: TSuccess;
    payload: TResponse;
}

export type RSAAIndexActionResponse<TRequest, TSuccess, TFailure, TObject> = RSAAResponseRequest<TRequest> |
    RSAAResponseFailure<TFailure> |
    RSAAResponseSuccess<TSuccess, JSONAPIListResponse<JSONAPIObject<TObject>> | JSONAPIErrorResponse>;

// Standardised JSON-API Index ActionCreator that fetches a resource child of some object / by relationship
export interface RSAAChildIndexActionRequest<TRequest, TSuccess, TFailure> {
    (parent_id: string, size?: number, pageNumber?: number, sort?: Array<string>, filters?: FlaskFilters): RSAAction<TRequest, TSuccess, TFailure>;
}

export interface RSAAReadActionRequest<TRequest, TSuccess, TFailure> {
    (id: string, include?: Array<string>): RSAAction<TRequest, TSuccess, TFailure>;
}

export interface RSAAReadActionResponseSuccess<TSuccess, TResponse> {
    type: TSuccess;
    payload: TResponse;
}

export type RSAAReadActionResponse<TRequest, TSuccess, TFailure, TResponse> = RSAAResponseRequest<TRequest> |
    RSAAResponseFailure<TFailure> | RSAAReadActionResponseSuccess<TSuccess, TResponse> | JSONAPIErrorResponse;


export interface RSAAPostActionRequest<TRequest, TSuccess, TFailure, TValues> {
    (values: TValues, relationships?: { [index: string]: JSONAPIRelationship[]; }): RSAAction<TRequest, TSuccess, TFailure>;
}

export type RSAAPostActionResponse<TRequest, TSuccess, TFailure, TResponse> = RSAAResponseRequest<TRequest> |
    RSAAResponseFailure<TFailure> | RSAAResponseSuccess<TSuccess, TResponse | JSONAPIErrorResponse>;

export interface RSAAPatchActionRequest<TRequest, TSuccess, TFailure, TValues> {
    (id: string, values: TValues): RSAAction<TRequest, TSuccess, TFailure>;
}

export interface RSAADeleteActionRequest<TRequest, TSuccess, TFailure> {
    (id: string): RSAAction<TRequest, TSuccess, TFailure>;
}

export interface RSAADeleteActionResponseSuccess<TSuccess> {
    type: TSuccess;
}

export type RSAADeleteActionResponse<TRequest, TSuccess, TFailure, TResponse> = RSAAResponseRequest<TRequest> |
    RSAAResponseFailure<TFailure> | RSAADeleteActionResponseSuccess<TSuccess>;

/**
 * This higher order function processes the standard JSON-API index action creator and provides the already encoded
 * URL query to be appended to the JSON-API endpoint URL.
 *
 * @param wrappedActionCreator
 */
export const encodeJSONAPIIndexParameters = <R>(wrappedActionCreator: WrappedIndexActionCreator<R>) => (
    size: number = 10,
    pageNumber: number = 1,
    sort?: Array<string>,
    filters?: FlaskFilters
) => {
    let queryParameters = [];

    queryParameters.push(`page[size]=${size}`);
    queryParameters.push(`page[number]=${pageNumber}`);

    if (sort && sort.length > 0) {
        queryParameters.push('sort=' + sort.join(','))
    }

    if (filters && filters.length > 0) {
        queryParameters.push('filter=' + JSON.stringify(filters));
    }

    return wrappedActionCreator(queryParameters);
};


/**
 * This higher order function processes the standard JSON-API index action creator and provides the already encoded
 * URL query to be appended to the JSON-API endpoint URL.
 *
 * @param wrappedActionCreator
 */
export const encodeJSONAPIChildIndexParameters = <R>(wrappedActionCreator: WrappedChildIndexActionCreator<R>) => (
    id: string,
    size: number = 10,
    pageNumber: number = 1,
    sort?: string[],
    filters?: FlaskFilters,
) => {
    let queryParameters = [];

    queryParameters.push(`page[size]=${size}`);
    queryParameters.push(`page[number]=${pageNumber}`);

    if (sort && sort.length > 0) {
        queryParameters.push('sort=' + sort.join(','))
    }

    if (filters && filters.length > 0) {
        queryParameters.push('filter=' + JSON.stringify(filters));
    }

    return wrappedActionCreator(id, queryParameters);
};