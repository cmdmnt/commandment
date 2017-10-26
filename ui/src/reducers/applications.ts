import {isJSONAPIErrorResponsePayload, JSONAPIObject} from "../json-api";
import {Application} from "../models";
import * as actions from "../actions/applications";

export interface ApplicationsState {
    items: Array<JSONAPIObject<Application>>;
    allIds: Array<string>;
    loading: boolean;
    error: boolean;
    errorDetail?: any
    lastReceived?: Date;
    currentPage: number;
    pageSize: number;
    recordCount?: number;
}

const initialState: ApplicationsState = {
    items: [],
    allIds: [],
    loading: false,
    error: false,
    errorDetail: null,
    lastReceived: null,
    currentPage: 1,
    pageSize: 50
};

type ApplicationsAction = actions.IndexActionResponse | actions.PostActionResponse | actions.PatchActionResponse;

export function applications (state: ApplicationsState = initialState, action: ApplicationsAction): ApplicationsState {
    switch (action.type) {
        case actions.INDEX_REQUEST:
            return {
                ...state,
                loading: true
            };
        case actions.INDEX_FAILURE:
            return {
                ...state,
                error: true,
                errorDetail: action.payload
            };
        case actions.INDEX_SUCCESS:
            if (isJSONAPIErrorResponsePayload(action.payload)) {
                return {
                    ...state,
                    loading: false,
                    error: true,
                    errorDetail: action.payload
                }
            } else {
                return {
                    ...state,
                    items: action.payload.data,
                    lastReceived: new Date,
                    loading: false,
                    recordCount: action.payload.meta.count
                };
            }
        default:
            return state;
    }
}