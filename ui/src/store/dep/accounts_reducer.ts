import {DEPAccount} from "./types";
import {DEPActions, DEPActionTypes} from "./actions";

import {isJSONAPIErrorResponsePayload, JSONAPIDataObject} from "../json-api";

export interface IDEPAccountsState {
    data?: Array<JSONAPIDataObject<DEPAccount>>;
    loading: boolean;
    submitted: boolean;
    error: boolean;
    errorDetail?: any;
}

const initialState: IDEPAccountsState = {
    error: false,
    loading: false,
    submitted: false,
};

// type VPPAction = TokenActionResponse;

export function accounts(state: IDEPAccountsState = initialState, action: DEPActions): IDEPAccountsState {
    switch (action.type) {
        case DEPActionTypes.ACCT_INDEX_REQUEST:
            return {
                ...state,
                loading: true,
            };
        case DEPActionTypes.ACCT_INDEX_SUCCESS:
            if (isJSONAPIErrorResponsePayload(action.payload)) {
                return {
                    ...state,
                    error: true,
                    errorDetail: action.payload,
                    loading: false,
                }
            } else {
                return {
                    ...state,
                    data: action.payload.data,
                    loading: false,
                };
            }
        case DEPActionTypes.ACCT_INDEX_FAILURE:
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
