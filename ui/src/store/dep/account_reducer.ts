import {Reducer} from "redux";
import {isJSONAPIErrorResponsePayload, JSONAPIDataObject} from "../json-api";
import {DEPActions, DEPActionTypes} from "./actions";
import {DEPAccount, DEPProfile} from "./types";

export interface IDEPAccountState {
    readonly dep_account?: JSONAPIDataObject<DEPAccount>;
    readonly dep_profiles?: Array<JSONAPIDataObject<DEPProfile>>;
    readonly loading: boolean;
    readonly error: boolean;
    readonly errorDetail?: any;
}

const initialState: IDEPAccountState = {
    error: false,
    loading: false,
};

export const account: Reducer<IDEPAccountState, DEPActions> = (state = initialState, action) => {
    switch (action.type) {

        case DEPActionTypes.ACCT_READ_REQUEST:
            return { ...state, loading: true };
        case DEPActionTypes.ACCT_READ_SUCCESS:
            const payload = action.payload;

            if (isJSONAPIErrorResponsePayload(payload)) {
                return {
                    ...state,
                    error: true,
                    errorDetail: payload,
                    loading: false,
                };
            } else {
                return {...state,
                    dep_account: payload.data,
                    dep_profiles: payload.included,
                    loading: false,
                };
            }
        case DEPActionTypes.ACCT_READ_FAILURE:
            return { ...state, loading: false, error: true, errorDetail: action.payload };

        default:
            return state;
    }
};
