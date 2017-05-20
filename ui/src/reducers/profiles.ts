import * as actions from '../actions/profiles';
import {IndexActionResponse} from '../actions/profiles';
import {isJSONAPIErrorResponsePayload} from "../constants";
import {PageProperties} from "griddle-react";

export interface ProfilesState {
    items: Array<JSONAPIObject<Profile>>;
    loading: boolean;
    error: boolean;
    errorDetail?: any
    lastReceived?: Date;
    pageProperties: PageProperties;
}

const initialState: ProfilesState = {
    items: [],
    loading: false,
    error: false,
    errorDetail: null,
    lastReceived: null,
    pageProperties: {
        currentPage: 1,
        pageSize: 10,
        recordCount: 0
    }
};

type ProfilesAction = IndexActionResponse;

export function profiles(state: ProfilesState = initialState, action: ProfilesAction): ProfilesState {
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