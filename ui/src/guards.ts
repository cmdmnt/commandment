// NOTE: Does not work with frames (but we don't have any)
import {ApiError} from "redux-api-middleware";

export const isArray = (v: any): v is Array<any> => v instanceof Array;
export const isApiError = (v: any): v is ApiError => v instanceof ApiError;

//// Type Guards
// import {ApiError, ErrorNames} from "redux-api-middleware";
//
// export function isApiError(payload: any): payload is ApiError {
//     return payload.name && payload.name === ErrorNames.ApiError;
// }
