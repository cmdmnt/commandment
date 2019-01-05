import {DEPActions, DEPActionTypes} from "./actions";
import {DEPProfile} from "./types";

import {isJSONAPIErrorResponsePayload, JSONAPIDataObject} from "../json-api";

export interface IDEPProfilesState {
    data?: Array<JSONAPIDataObject<DEPProfile>>;
    loading: boolean;
    submitted: boolean;
    error: boolean;
    errorDetail?: any;
}

const initialState: IDEPProfilesState = {
    loading: false,
    error: false,
    submitted: false,
};

// type VPPAction = TokenActionResponse;

export function profiles(state: IDEPProfilesState = initialState, action: DEPActions): IDEPProfilesState {
    switch (action.type) {
        case DEPActionTypes.PROF_INDEX_REQUEST:
            return {
                ...state,
                loading: true,
            };
        case DEPActionTypes.PROF_INDEX_SUCCESS:
            if (isJSONAPIErrorResponsePayload(action.payload)) {
                return {
                    ...state,
                    loading: false,
                    error: true,
                    errorDetail: action.payload,
                };
            } else {
                return {
                    ...state,
                    loading: false,
                    data: action.payload.data,
                };
            }
        case DEPActionTypes.PROF_INDEX_FAILURE:
            return {
                ...state,
                loading: false,
                error: true,
                errorDetail: action.payload,
            };

        default:
            return state;
    }
}
