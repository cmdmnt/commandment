import {DEPActions, DEPActionTypes} from "./actions";
import {DEPProfile} from "./types";

import {isJSONAPIErrorResponsePayload, JSONAPIDataObject} from "../json-api";

export interface IDEPProfilesState {
    data?: Array<JSONAPIDataObject<DEPProfile>>;
    error: boolean;
    errorDetail?: any;
    loading: boolean;
    submitted: boolean;
}

const initialState: IDEPProfilesState = {
    error: false,
    loading: false,
    submitted: false,
};

// type VPPAction = ITokenActionResponse;

export function profiles(state: IDEPProfilesState = initialState, action: DEPActions): IDEPProfilesState {
    switch (action.type) {
        case DEPActionTypes.PROF_INDEX_REQUEST:
            return {
                ...state,
                loading: true,
            };
        case DEPActionTypes.PROF_INDEX_SUCCESS:
            const payload = action.payload;
            if (isJSONAPIErrorResponsePayload(payload)) {
                return {
                    ...state,
                    error: true,
                    errorDetail: payload,
                    loading: false,
                };
            } else {
                return {
                    ...state,
                    data: payload.data,
                    loading: false,
                };
            }
        case DEPActionTypes.PROF_INDEX_FAILURE:
            return {
                ...state,
                error: true,
                errorDetail: action.payload,
                loading: false,
            };

        default:
            return state;
    }
}
