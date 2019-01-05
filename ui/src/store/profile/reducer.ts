import {isJSONAPIErrorResponsePayload, JSONAPIDataObject} from "../json-api";
import {PatchRelationshipActionResponse, ReadActionResponse} from "../profiles/actions";
import {ProfilesActionTypes} from "../profiles/actions";
import {Profile} from "../profiles/types";
import {Tag} from "../tags/types";

export interface IProfileState {
    profile?: JSONAPIDataObject<Profile>;
    loading: boolean;
    error: boolean;
    errorDetail?: any
    tags?: Array<JSONAPIDataObject<Tag>>;
    tagsLoading: boolean;
}

const initialState: IProfileState = {
    error: false,
    errorDetail: null,
    loading: false,
    profile: null,
    tagsLoading: false,
};

type ProfileAction = ReadActionResponse | PatchRelationshipActionResponse;

export function profile(state: IProfileState = initialState, action: ProfileAction): IProfileState {
    switch (action.type) {
        case ProfilesActionTypes.READ_REQUEST:
            return {
                ...state,
                loading: true,
            };

        case ProfilesActionTypes.READ_FAILURE:
            return {
                ...state,
                error: true,
                errorDetail: action.payload,
            };

        case ProfilesActionTypes.READ_SUCCESS:
            if (isJSONAPIErrorResponsePayload(action.payload)) {
                return {
                    ...state,
                    error: true,
                    errorDetail: action.payload,
                }
            } else {
                let tags: Array<JSONAPIDataObject<Tag>> = [];

                if (action.payload.included) {
                    tags = action.payload.included.filter((included: JSONAPIDataObject<any>) => (included.type === "tags"));
                }

                return {
                    ...state,
                    profile: action.payload.data,
                    loading: false,
                    tags,
                };
            }
        case ProfilesActionTypes.REL_PATCH_REQUEST:
            return {
                ...state,
                tagsLoading: true,
            };
        case ProfilesActionTypes.REL_PATCH_SUCCESS:
            if (isJSONAPIErrorResponsePayload(action.payload)) {
                return {
                    ...state,
                    error: true,
                    errorDetail: action.payload,
                }
            } else {
                const profile: JSONAPIDataObject<Profile> = {
                    ...state.profile,
                    relationships: {
                        ...state.profile.relationships,
                        tags: action.payload.data.relationships.tags,
                    },
                };

                return {
                    ...state,
                    profile,
                    tagsLoading: false,
                };
            }

        case ProfilesActionTypes.REL_PATCH_FAILURE:
            return {
                ...state,
                tagsLoading: false,
            };
        default:
            return state;
    }
}
