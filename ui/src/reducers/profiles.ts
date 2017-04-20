import * as actions from '../actions/profiles';
import {IndexActionResponse} from '../actions/profiles';

export interface ProfilesState {
    items: Array<JSONAPIObject<Profile>>;
    loading: boolean;
    error: boolean;
    errorDetail?: any
    lastReceived?: Date;
    currentPage: number;
    pageSize: number;
    recordCount?: number;
}

const initialState: ProfilesState = {
    items: [],
    loading: false,
    error: false,
    errorDetail: null,
    lastReceived: null,
    currentPage: 1,
    pageSize: 50
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
            return {
                ...state,
                items: action.payload.data,
                lastReceived: new Date,
                loading: false,
                recordCount: action.payload.meta.count
            };

        default:
            return state;
    }
}