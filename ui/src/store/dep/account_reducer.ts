import {Reducer} from "redux";
import {isJSONAPIErrorResponsePayload, JSONAPIDataObject} from "../../json-api";
import {DEPActions, DEPActionTypes} from "./actions";
import {DEPAccount, DEPProfile} from "./types";

export interface DEPAccountState {
    readonly dep_account?: JSONAPIDataObject<DEPAccount>;
    readonly dep_profiles?: Array<JSONAPIDataObject<DEPProfile>>;
    readonly loading: boolean;
    readonly error: boolean;
    readonly errorDetail?: any;
}

const initialState: DEPAccountState = {
    error: false,
    loading: false,
};

export const account: Reducer<DEPAccountState, DEPActions> = (state = initialState, action) => {
    switch (action.type) {

        case DEPActionTypes.ACCT_READ_REQUEST:
            return { ...state, loading: true };
        case DEPActionTypes.ACCT_READ_SUCCESS:
            if (isJSONAPIErrorResponsePayload(action.payload)) {
                return {
                    ...state,
                    loading: false,
                    error: true,
                    errorDetail: action.payload,
                };
            } else {
                return {...state,
                    loading: false,
                    dep_account: action.payload.data,
                    dep_profiles: action.payload.included};
            }
        case DEPActionTypes.ACCT_READ_FAILURE:
            return { ...state, loading: false, error: true, errorDetail: action.payload };

        default:
            return state;
    }
};
