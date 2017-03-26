import {Store, Dispatch} from "react-redux";
import {Middleware} from "redux";


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

declare function getJSON(res: Response): PromiseLike<any>;

declare function apiMiddleware<S>(store: Store): (next: Dispatch<S>) => Dispatch<S>;

declare type HTTPVerb = 'GET' | 'HEAD' | 'POST' | 'PUT' | 'PATCH' | 'DELETE' | 'OPTIONS';

interface TypeDescriptor<TSymbol> {
    type: string | TSymbol;
    payload: any;
    meta: any;
}


//declare type CALL_API = Symbol('CALL_API');

declare interface RSAA<R, S, F> {
    CALL_API: {
        endpoint: string;  // or function
        method: HTTPVerb;
        body?: any;
        headers?: string; // or function
        credentials?: 'omit' | 'same-origin' | 'include';
        bailout?: boolean; // or function
        types: [R, S, F];
    }
}
