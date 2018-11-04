import {Reducer} from 'redux';
import {isJSONAPIErrorResponsePayload, JSONAPIObject} from "../../json-api";
import {DEPAccount} from "./types";
import {DEPActions, DEPActionTypes} from "./actions";

export interface DEPAccountState {
    readonly dep_account?: JSONAPIObject<DEPAccount>;
    readonly loading: boolean;
    readonly error: boolean;
    readonly errorDetail?: any
}

const initialState: DEPAccountState = {
    loading: false,
    error: false,
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
                    errorDetail: action.payload
                }
            } else {
                return {...state, loading: false, dep_account: action.payload.data};
            }
        case DEPActionTypes.ACCT_READ_FAILURE:
            return { ...state, loading: false, error: true, errorDetail: action.payload };

        default:
            return state;
    }
};
