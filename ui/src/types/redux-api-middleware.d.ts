import {Store} from "react-redux";

declare module "redux-api-middleware" {

    export const CALL_API = Symbol('CALL_API');

    // validation
    declare function isRSAA(action: any): boolean;

    // Returns array of strings containing validation errors
    declare function validateRSAA(action: any): Array<string>;
    declare function isValidRSAA(action: any): boolean;

    declare class InvalidRSAA {
        constructor(validationErrors: Array<string>);

        name: string;
        message: string;
        validationErrors: Array<string>;
    }

    declare class InternalError {
        constructor(message: string);

        name: string;
        message: string;
    }

    declare class RequestError {
        constructor(message: string);

        name: string;
        message: string;
    }

    declare class ApiError {
        constructor(status: number, statusText: string, response: any);

        name: string;
        message: string;
        status: number;
        statusText: string;
        response?: any;
    }

    declare function getJSON(res: Response): PromiseLike;

    declare function apiMiddleware(store: Store);

    declare type HTTPVerb = 'GET' | 'HEAD' | 'POST' | 'PUT' | 'PATCH' | 'DELETE' | 'OPTIONS';

    declare interface TypeDescriptor<TSymbol> {
        type: string | TSymbol;
        payload: any;
        meta: any;
    }
    
    declare interface RSAA<R, S, F> {
        [propName: CALL_API]: {
            endpoint: string | () => void;
            method: HTTPVerb;
            body?: any;
            headers?: string | () => void;
            credentials?: 'omit' | 'same-origin' | 'include';
            bailout?: boolean | () => void;
            types: [R, S, F];
        }
    }
}