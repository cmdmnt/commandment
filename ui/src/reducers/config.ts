import * as actions from '../actions/config';
import {POST_REQUEST} from "../actions/config";
import {POST_FAILURE} from "../actions/config";
import {POST_SUCCESS} from "../actions/config";

export interface ConfigState {
    config?: JSONAPIObject<MDMConfig>;
    loading: boolean;
    error: boolean;
    errorDetail?: any
    lastReceived?: Date;
}

const initialState: ConfigState = {
    loading: false,
    error: false
};

export function config(state: ConfigState = initialState, action: actions.PostActionResponse): ConfigState {
    switch (action.type) {
        case POST_REQUEST:
            return {
                ...state,
                loading: true
            };
        case POST_FAILURE:
            return {
                ...state,
                loading: false,
                error: true,
                errorDetail: action.payload
            };
        case POST_SUCCESS:
            return {
                ...state,
                loading: false,
                config: action.payload.data
            };
        default:
            return state;
    }
}