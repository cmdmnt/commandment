import {Tag} from "../models";
import {isJSONAPIErrorResponsePayload, JSONAPIErrorResponse, JSONAPIDataObject} from "../json-api";
import {IndexActionResponse, INDEX_REQUEST, INDEX_SUCCESS, INDEX_FAILURE} from "../actions/tags";

export interface TagsState {
    loading: boolean;
    items: Array<JSONAPIDataObject<Tag>>;
    error: boolean;
    errorDetail?: JSONAPIErrorResponse;
}

const initialState: TagsState = {
    loading: false,
    items: [],
    error: false
};

type TagsAction = IndexActionResponse;

export function tags(state: TagsState = initialState, action: TagsAction): TagsState {
    switch (action.type) {
        case INDEX_REQUEST:
            return {
                ...state,
                loading: true
            };
        case INDEX_SUCCESS:
            if (isJSONAPIErrorResponsePayload(action.payload)) {
                return {
                    ...state,
                    error: true,
                    errorDetail: action.payload
                }
            } else {
                return {
                    ...state,
                    items: action.payload.data,
                    loading: false
                };
            }
        case INDEX_FAILURE:
            return {
                ...state,
                error: true,
                loading: false
            };
        default:
            return state;
    }
}