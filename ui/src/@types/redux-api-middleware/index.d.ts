declare module "redux-api-middleware" {
    import {Action, AnyAction, Middleware} from "redux";
    /**
     * Symbol key that carries API call info interpreted by this Redux middleware.
     *
     * @constant {string}
     * @access public
     * @default
     */
    export const RSAA: string;
    export type RSAA = "@@redux-api-middleware/RSAA";

//// ERRORS

    export enum ErrorNames {
        ApiError = "ApiError",
        InternalError = "InternalError",
        InvalidRSAA = "InvalidRSAA",
        RequestError = "RequestError",
    }

    /**
     * Error class for an RSAA that does not conform to the RSAA definition
     *
     * @class InvalidRSAA
     * @access public
     * @param {array} validationErrors - an array of validation errors
     */
    export class InvalidRSAA extends Error {
        public name: ErrorNames.InvalidRSAA;
        public message: string;
        public validationErrors: string[];

        constructor(validationErrors: string[]);
    }

    /**
     * Error class for a custom `payload` or `meta` function throwing
     *
     * @class InternalError
     * @access public
     * @param {string} message - the error message
     */
    export class InternalError extends Error {
        public name: ErrorNames.InternalError;
        public message: string;

        constructor(message: string);
    }

    /**
     * Error class for an error raised trying to make an API call
     *
     * @class RequestError
     * @access public
     * @param {string} message - the error message
     */
    export class RequestError extends Error {
        public name: ErrorNames.RequestError;
        public message: string;

        constructor(message: string);
    }

    /**
     * Error class for an API response outside the 200 range
     *
     * @class ApiError
     * @access public
     * @param {number} status - the status code of the API response
     * @param {string} statusText - the status text of the API response
     * @param {object} response - the parsed JSON response of the API server if the
     *  'Content-Type' header signals a JSON response
     */
    export class ApiError<R = any> extends Error {
        public name: ErrorNames.ApiError;
        public message: string;
        public status: number;
        public statusText: string;
        public response?: R;

        constructor(status: number, statusText: string, response: R);
    }

//// VALIDATION

    /**
     * Is the given action a plain JavaScript object with a [RSAA] property?
     */
    export function isRSAA(action: any): action is RSAAction<any, any, any>;

    /**
     * The README explains the following criteria for a TypeDescriptor:
     *
     * A type descriptor **MUST**:
     * - be a plain JavaScript object
     * - have a `type` property, which **MUST** be a string or a `Symbol`.
     */
    export interface TypeDescriptor<TSymbol, TPayload = any, TMeta = any> {
        type: string | TSymbol;
        payload?: TPayload;
        meta?: TMeta;
    }

    /**
     * Is the given object a valid type descriptor?
     */
    export function isValidTypeDescriptor(obj: object): obj is TypeDescriptor<any>;

    /**
     * Checks an action against the RSAA definition, returning a (possibly empty)
     * array of validation errors.
     */
    export function validateRSAA(action: any): string[];

    /**
     * Is the given action a valid RSAA?
     */
    export function isValidRSAA(action: any): boolean;

//// MIDDLEWARE

    export interface MiddlewareOptions {
        // Determines whether the response is an error
        ok: (res: any) => boolean;
        fetch: GlobalFetch;
    }

    /**
     * Create middleware with custom options.
     */
    export function createMiddleware(options?: MiddlewareOptions): Middleware;

    /**
     * A Redux middleware that processes RSAA actions.
     */
    export const apiMiddleware: Middleware;

//// UTIL

    /**
     * Extract JSON body from a server response
     */
    export function getJSON(res: Response): PromiseLike<any> | undefined;

    export type RSAActionTypeTuple = [string | symbol, string | symbol, string | symbol];

    /**
     * Blow up string or symbol types into full-fledged type descriptors,
     *   and add defaults
     */
    export function normalizeTypeDescriptors(types: RSAActionTypeTuple): RSAActionTypeTuple;

    export type HTTPVerb = "GET" | "HEAD" | "POST" | "PUT" | "PATCH" | "DELETE" | "OPTIONS";

    export interface RSAActionBody<R, S, F> {
        endpoint: string;  // or function
        method: HTTPVerb;
        body?: any;
        headers?: { [propName: string]: string }; // or function
        credentials?: "omit" | "same-origin" | "include";
        bailout?: boolean; // or function
        types: [R, S, F];
    }

    export enum Credentials {
        omit = "omit",
        sameOrigin = "same-origjn",
        include = "include",
    }

    export type RSAAActionType = string | TypeDescriptor<any>;
    export type RSAAActionTypes = [RSAAActionType, RSAAActionType, RSAAActionType];

    export interface RSAAction<TRequest, TSuccess, TFail> {
        [propName: string]: { // Symbol as object key seems impossible
            endpoint: string;  // or function
            method: HTTPVerb;
            types: [TRequest, TSuccess, TFail];
            body?: any;
            headers?: any; // or function
            options?: any;
            credentials?: Credentials;
            bailout?: boolean; // or function
            fetch?: GlobalFetch;
            ok?: any;
        }
    }

    //// Augmentations

    module "redux" {
        export interface AnyAction {
            "@@redux-api-middleware/RSAA"?: RSAActionBody<any, any, any>;
        }
    }
}
