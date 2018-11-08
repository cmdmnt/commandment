
import * as actions from '../actions/profiles';
import {Profile, Tag} from "../models";
import {isJSONAPIErrorResponsePayload, JSONAPIDataObject} from "../json-api";
import {PatchRelationshipActionResponse, ReadActionResponse} from "../actions/profiles";

export interface ProfileState {
    profile?: JSONAPIDataObject<Profile>;
    loading: boolean;
    error: boolean;
    errorDetail?: any
    tags?: Array<JSONAPIDataObject<Tag>>;
    tagsLoading: boolean;
}

const initialState: ProfileState = {
    profile: null,
    loading: false,
    tagsLoading: false,
    error: false,
    errorDetail: null
};

type ProfileAction = ReadActionResponse | PatchRelationshipActionResponse;


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
                let tags: Array<JSONAPIDataObject<Tag>> = [];

                if (action.payload.included) {
                    tags = action.payload.included.filter((included: JSONAPIDataObject<any>) => (included.type === 'tags'));
                }

                return {
                    ...state,
                    profile: action.payload.data,
                    loading: false,
                    tags
                };
            }
        case actions.RPATCH_REQUEST:
            return {
                ...state,
                tagsLoading: true
            };
        case actions.RPATCH_SUCCESS:
            if (isJSONAPIErrorResponsePayload(action.payload)) {
                return {
                    ...state,
                    error: true,
                    errorDetail: action.payload
                }
            } else {
                const profile: JSONAPIDataObject<Profile> = {
                    ...state.profile,
                    relationships: {
                        ...state.profile.relationships,
                        tags: action.payload.data.relationships.tags
                    }
                };

                return {
                    ...state,
                    profile,
                    tagsLoading: false
                };
            }

        case actions.RPATCH_FAILURE:
            return {
                ...state,
                tagsLoading: false
            };
        default:
            return state;
    }
}