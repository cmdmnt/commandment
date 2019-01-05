import {isJSONAPIErrorResponsePayload, JSONAPIDataObject, JSONAPIErrorResponse} from "../json-api";
import {Tag} from "./types";
import {IndexActionResponse, TagsActionTypes} from "./actions";

export interface ITagsState {
    loading: boolean;
    items: Array<JSONAPIDataObject<Tag>>;
    error: boolean;
    errorDetail?: JSONAPIErrorResponse;
}

const initialState: ITagsState = {
    error: false,
    items: [],
    loading: false,
};

type TagsAction = IndexActionResponse;

export function tags(state: ITagsState = initialState, action: TagsAction): ITagsState {
    switch (action.type) {
        case TagsActionTypes.INDEX_REQUEST:
            return {
                ...state,
                loading: true,
            };
        case TagsActionTypes.INDEX_SUCCESS:
            if (isJSONAPIErrorResponsePayload(action.payload)) {
                return {
                    ...state,
                    error: true,
                    errorDetail: action.payload,
                }
            } else {
                return {
                    ...state,
                    error: false,
                    items: action.payload.data,
                    loading: false,
                };
            }
        case TagsActionTypes.INDEX_FAILURE:
            return {
                ...state,
                error: true,
                loading: false,
            };
        default:
            return state;
    }
}
