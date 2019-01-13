import {ApiError} from "redux-api-middleware";

/**
 * This interface declares a common interface for reducers that contain an array of results and metadata about those
 * results.
 */
export interface IResults<TResultArray> {
    items: TResultArray;
    loading: boolean;
    error?: ApiError | any;
    lastReceived?: Date;
    currentPage: number;
    pageSize: number;
    pages: number;
    recordCount?: number;
}

export const ResultsDefaultState: IResults<any> = {
    currentPage: 1,
    error: null,
    items: [],
    lastReceived: null,
    loading: false,
    pageSize: 20,
    pages: 0,
    recordCount: 0,
};
