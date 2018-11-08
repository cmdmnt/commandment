import {Reducer} from "redux";
import {isJSONAPIErrorResponsePayload, JSONAPIDataObject} from "../../json-api";
import {DEPActions, DEPActionTypes} from "./actions";
import {DEPProfile} from "./types";

export interface IDEPProfileState {
    readonly dep_profile?: JSONAPIDataObject<DEPProfile>;
    readonly loading: boolean;
    readonly error: boolean;
    readonly errorDetail?: any;
}

const initialState: IDEPProfileState = {
    loading: false,
    error: false,
};

export const profile: Reducer<IDEPProfileState, DEPActions> = (state = initialState, action) => {
    switch (action.type) {

        case DEPActionTypes.PROF_READ_REQUEST:
            return { ...state, loading: true };
        case DEPActionTypes.PROF_READ_SUCCESS:
            if (isJSONAPIErrorResponsePayload(action.payload)) {
                return {
                    ...state,
                    loading: false,
                    error: true,
                    errorDetail: action.payload,
                };
            } else {
                return {...state, loading: false, dep_account: action.payload.data};
            }
        case DEPActionTypes.PROF_READ_FAILURE:
            return { ...state, loading: false, error: true, errorDetail: action.payload };

        case DEPActionTypes.PROF_POST_REQUEST:
            return { ...state, loading: true };
        case DEPActionTypes.PROF_POST_SUCCESS:
            if (isJSONAPIErrorResponsePayload(action.payload)) {
                return {
                    ...state,
                    loading: false,
                    error: true,
                    errorDetail: action.payload,
                };
            } else {
                return {...state, loading: false, dep_account: action.payload.data};
            }
        case DEPActionTypes.PROF_POST_FAILURE:
            return { ...state, loading: false, error: true, errorDetail: action.payload };

        default:
            return state;
    }
};
