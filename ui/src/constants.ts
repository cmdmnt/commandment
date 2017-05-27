import {FlaskFilters} from "./actions/constants";
import {JSONAPIDetailResponse, JSONAPIErrorResponse, JSONAPIListResponse, JSONAPIObject} from "./typings/definitions";
import {RSAA} from "redux-api-middleware";

export const CERTIFICATE_PURPOSE: {[propName: string]:string} = {
    'mdm.pushcert': 'APNS MDM Push Certificate',
    'mdm.webcrt': 'MDM Web Server Certificate',
    'mdm.cacert': 'MDM SCEP CA Certificate'
};

// Redux API Middleware Type Guards

export function isJSONAPIErrorResponsePayload(
    payload: JSONAPIListResponse<any> |
        JSONAPIDetailResponse<any, any> |
        JSONAPIErrorResponse): payload is JSONAPIErrorResponse {

    return (<JSONAPIErrorResponse>payload).errors !== undefined;
}


interface WrappedChildIndexActionCreator<R> {
    (id: number, queryParameters: Array<String>): R;
}

interface WrappedIndexActionCreator<R> {
    (queryParameters: Array<String>): R;
}

// Standardised JSON-API Index ActionCreator
export interface RSAAIndexActionRequest<TRequest, TSuccess, TFailure> {
    (size?: number, pageNumber?: number, sort?: Array<string>, filters?: FlaskFilters): RSAA<TRequest, TSuccess, TFailure>;
}

// Standardised JSON-API Index ActionCreator Response (passed to reducer)
export interface RSAAIndexActionResponse<TRequest, TSuccess, TFailure, TObject> {
    type: TRequest | TSuccess | TFailure;
    payload?: JSONAPIListResponse<JSONAPIObject<TObject>> | JSONAPIErrorResponse;
}

// Standardised JSON-API Index ActionCreator that fetches a resource child of some object / by relationship
export interface RSAAChildIndexActionRequest<TRequest, TSuccess, TFailure> {
    (parent_id: number, size?: number, pageNumber?: number, sort?: Array<string>, filters?: FlaskFilters): RSAA<TRequest, TSuccess, TFailure>;
}

export interface RSAAReadActionRequest<TRequest, TSuccess, TFailure> {
    (id: number, include?: Array<string>): RSAA<TRequest, TSuccess, TFailure>;
}

export interface RSAAReadActionResponse<TRequest, TSuccess, TFailure, TResponse> {
    type: TRequest | TSuccess | TFailure;
    payload: TResponse | JSONAPIErrorResponse;
}

/**
 * This higher order function processes the standard JSON-API index action creator and provides the already encoded
 * URL query to be appended to the JSON-API endpoint URL.
 *
 * @param wrappedActionCreator
 */
export const encodeJSONAPIIndexParameters = <R>(wrappedActionCreator: WrappedIndexActionCreator<R>) => (
    size: number = 10,
    pageNumber: number = 1,
    sort?: [String],
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
    id: number,
    size: number = 10,
    pageNumber: number = 1,
    sort?: [String],
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

    return wrappedActionCreator(id, queryParameters);
};