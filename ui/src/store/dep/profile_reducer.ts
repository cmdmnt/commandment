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
    error: false,
    loading: false,
};

export const profile: Reducer<IDEPProfileState, DEPActions> = (state = initialState, action) => {
    switch (action.type) {

        case DEPActionTypes.PROF_READ_REQUEST:
            return { ...state, loading: true };
        case DEPActionTypes.PROF_READ_SUCCESS:
            if (isJSONAPIErrorResponsePayload(action.payload)) {
                return {
                    ...state,
                    error: true,
                    errorDetail: action.payload,
                    loading: false,
                };
            } else {
                return {
                    ...state,
                    dep_profile: action.payload.data,
                    loading: false,
                };
            }
        case DEPActionTypes.PROF_READ_FAILURE:
            return { ...state, loading: false, error: true, errorDetail: action.payload };

        case DEPActionTypes.PROF_POST_REQUEST:
            return { ...state, loading: true };
        case DEPActionTypes.PROF_POST_SUCCESS:
            if (isJSONAPIErrorResponsePayload(action.payload)) {
                return {
                    ...state,
                    error: true,
                    errorDetail: action.payload,
                    loading: false,
                };
            } else {
                return {
                    ...state,
                    dep_account: action.payload.data,
                    loading: false,
                };
            }
        case DEPActionTypes.PROF_POST_FAILURE:
            return { ...state, loading: false, error: true, errorDetail: action.payload };

        default:
            return state;
    }
};
