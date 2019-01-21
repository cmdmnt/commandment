import {Reducer} from "redux";
import {isJSONAPIErrorResponsePayload, JSONAPIDataObject, RSAAResponseSuccess} from "../json-api";
import {DEPActions, DEPActionTypes} from "./actions";
import {DEPProfile} from "./types";
import {isApiError} from "../../guards";

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
            return {
                ...state,
                loading: true,
                error: false,
                errorDetail: null,
                dep_profile: null,
            };
        case DEPActionTypes.PROF_READ_SUCCESS:
            let payload = action.payload;
            if (isApiError(payload)) {
                return {
                    ...state,
                    error: true,
                    errorDetail: payload,
                    loading: false,
                }
            } else if (isJSONAPIErrorResponsePayload(payload)) {
                return {
                    ...state,
                    error: true,
                    errorDetail: action.payload,
                    loading: false,
                };
            } else {
                return {
                    ...state,
                    dep_profile: payload.data,
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

        case DEPActionTypes.PROF_PATCH_REQUEST:
            return { ...state, loading: true };
        case DEPActionTypes.PROF_PATCH_SUCCESS:
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
                    dep_account: payload.data,
                    loading: false,
                };
            }
        case DEPActionTypes.PROF_PATCH_FAILURE:
            return { ...state, loading: false, error: true, errorDetail: action.payload };

        default:
            return state;
    }
};
