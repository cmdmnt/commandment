// Standardised JSON-API Index ActionCreator Response (passed to reducer)

import {Action} from "redux";
import {ApiError, InvalidRSAA, RequestError, RSAAction} from "redux-api-middleware";
import {JSONAPIDataObject, JSONAPIErrorResponse, JSONAPIListResponse} from "./json-api";
import {JSONAPIDocument, Relationships} from "../json-api-v1";
import {FlaskFilters} from "../flask-rest-jsonapi";


export interface RSAARequestAction<TRequest> extends Action<TRequest> {
    error?: boolean;
    payload?: InvalidRSAA | RequestError;
    type: TRequest;
}

export interface RSAAFailureAction<TFailure> extends Action<TFailure> {
    payload: ApiError;
    type: TFailure;
}

// Success can still contain API errors that are 2xx responses
export interface RSAASuccessAction<TSuccess, TResponse> extends Action<TSuccess> {
    payload: TResponse;
    type: TSuccess;
}

export type RSAAActionResponse<TRequest, TSuccess, TFailure, TData, TIncluded> =
    RSAARequestAction<TRequest> |
    RSAAFailureAction<TFailure> |
    RSAASuccessAction<TSuccess, JSONAPIDocument<TData, TIncluded>>;

// Standardised JSON-API Index ActionCreator
export type RSAAIndexActionCreator<TRequest, TSuccess, TFailure> =
    (size?: number, pageNumber?: number, sort?: string[], filters?: FlaskFilters) =>
        RSAAction<TRequest, TSuccess, TFailure>;

export type RSAAReadActionCreator<TRequest, TSuccess, TFailure> = (id: string, include?: string[])
    => RSAAction<TRequest, TSuccess, TFailure>;

export type RSAAPostActionCreator<TRequest, TSuccess, TFailure, TValues> =
    (values: TValues, relationships?: Relationships) =>
    RSAAction<TRequest, TSuccess, TFailure>;

export type RSAAPatchActionCreator<TRequest, TSuccess, TFailure, TValues> = (id: string, values: Partial<TValues>)
    => RSAAction<TRequest, TSuccess, TFailure>;
