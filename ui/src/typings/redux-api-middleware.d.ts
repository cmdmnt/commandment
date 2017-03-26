declare module "redux-api-middleware" {

    import {Store, Dispatch} from "react-redux";
    import {Middleware} from "redux";

// validation
    function isRSAA(action: any): boolean;

// Returns array of strings containing validation errors
    function validateRSAA(action: any): Array<string>;

    function isValidRSAA(action: any): boolean;

    class InvalidRSAA {
        constructor(validationErrors: Array<string>);

        name: string;
        message: string;
        validationErrors: Array<string>;
    }

    class InternalError {
        constructor(message: string);

        name: string;
        message: string;
    }

    class RequestError {
        constructor(message: string);

        name: string;
        message: string;
    }

    class ApiError {
        constructor(status: number, statusText: string, response: any);

        name: string;
        message: string;
        status: number;
        statusText: string;
        response?: any;
    }

    function getJSON(res: Response): PromiseLike<any>;

    function apiMiddleware<S>(store: Store<any>): (next: Dispatch<S>) => Dispatch<S>;

    type HTTPVerb = 'GET' | 'HEAD' | 'POST' | 'PUT' | 'PATCH' | 'DELETE' | 'OPTIONS';

    interface TypeDescriptor<TSymbol> {
        type: string | TSymbol;
        payload: any;
        meta: any;
    }

    
    //type CALL_API = Symbol('CALL_API');
    export const CALL_API = 'CALL_API'; // Cheating for now

    interface RSAA<R, S, F> {
        [propName: string]: { // Symbol as object key seems impossible
            endpoint: string;  // or function
            method: HTTPVerb;
            body?: any;
            headers?: { [propName: string]: string }; // or function
            credentials?: 'omit' | 'same-origin' | 'include';
            bailout?: boolean; // or function
            types: [R, S, F];
        }
    }

}