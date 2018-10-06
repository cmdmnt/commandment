// import * as actions from "../../actions/vpp";
import {DEPAccount} from "../../models";
// import {TokenActionResponse} from "../../actions/vpp";
import {DEPActions, DEPActionTypes} from "../../actions/settings/dep";

import {isJSONAPIErrorResponsePayload, JSONAPIObject} from "../../json-api";

export interface DEPState {
    data?: Array<JSONAPIObject<DEPAccount>>;
    loading: boolean;
    submitted: boolean;
    error: boolean;
    errorDetail?: any;
}

const initialState: DEPState = {
    loading: false,
    error: false,
    submitted: false
};

// type VPPAction = TokenActionResponse;

export function dep(state: DEPState = initialState, action: DEPActions): DEPState {
    switch (action.type) {
        case DEPActionTypes.INDEX_REQUEST:
            return {
                ...state,
                loading: true
            };
        case DEPActionTypes.INDEX_SUCCESS:
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
                    loading: false,
                    data: action.payload.data
                };
            }
        case DEPActionTypes.INDEX_FAILURE:
            return {
                ...state,
                loading: false,
                error: true,
                errorDetail: action.payload
            };

        default:
            return state;
    }
}