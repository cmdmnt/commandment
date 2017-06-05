
import * as actions from '../actions/profiles';
import {Profile, Tag} from "../models";
import {isJSONAPIErrorResponsePayload, JSONAPIObject} from "../json-api";
import {ReadActionResponse} from "../actions/profiles";

export interface ProfileState {
    profile?: JSONAPIObject<Profile>;
    loading: boolean;
    error: boolean;
    errorDetail?: any
    tags?: Array<JSONAPIObject<Tag>>;
    tagsLoading: boolean;
}

const initialState: ProfileState = {
    profile: null,
    loading: false,
    tagsLoading: false,
    error: false,
    errorDetail: null
};

type ProfileAction = ReadActionResponse;


export function profile(state: ProfileState = initialState, action: ProfileAction): ProfileState {
    switch (action.type) {
        case actions.READ_REQUEST:
            return {
                ...state,
                loading: true
            };

        case actions.READ_FAILURE:
            return {
                ...state,
                error: true,
                errorDetail: action.payload
            };

        case actions.READ_SUCCESS:
            if (isJSONAPIErrorResponsePayload(action.payload)) {
                return {
                    ...state,
                    error: true,
                    errorDetail: action.payload
                }
            } else {
                let tags: Array<JSONAPIObject<Tag>> = [];

                if (action.payload.included) {
                    tags = action.payload.included.filter((included: JSONAPIObject<any>) => (included.type === 'tags'));
                }

                return {
                    ...state,
                    profile: action.payload.data,
                    lastReceived: new Date,
                    loading: false,
                    tags
                };
            }
        default:
            return state;
    }
}