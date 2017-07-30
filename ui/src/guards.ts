// NOTE: Does not work with frames (but we don't have any)
import {ApiError} from "redux-api-middleware";

export const isArray = (v: any): v is Array<any> => v instanceof Array;
export const isApiError = (v: any): v is ApiError => v instanceof ApiError;