import {DEPAccount} from "./types";
import {DEPActions, DEPActionTypes} from "./actions";

import {isJSONAPIErrorResponsePayload, JSONAPIObject} from "../../json-api";

export interface IDEPAccountsState {
    data?: Array<JSONAPIObject<DEPAccount>>;
    loading: boolean;
    submitted: boolean;
    error: boolean;
    errorDetail?: any;
}

const initialState: IDEPAccountsState = {
    loading: false,
    error: false,
    submitted: false
};

// type VPPAction = TokenActionResponse;

export function accounts(state: IDEPAccountsState = initialState, action: DEPActions): IDEPAccountsState {
    switch (action.type) {
        case DEPActionTypes.ACCT_INDEX_REQUEST:
            return {
                ...state,
                loading: true
            };
        case DEPActionTypes.ACCT_INDEX_SUCCESS:
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
        case DEPActionTypes.ACCT_INDEX_FAILURE:
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
