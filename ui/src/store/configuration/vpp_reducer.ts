import {isJSONAPIErrorResponsePayload, JSONAPIDetailResponse} from "../json-api";
import {VPPAccount} from "./types";
import {TokenActionResponse, VPPActionTypes} from "./vpp";

export interface VPPState {
    data?: JSONAPIDetailResponse<VPPAccount, void>;
    loading: boolean;
    submitted: boolean;
    error: boolean;
    errorDetail?: any;
}

const initialState: VPPState = {
    error: false,
    loading: false,
    submitted: false,
};

type VPPAction = TokenActionResponse;

export function vpp(state: VPPState = initialState, action: VPPAction): VPPState {
    switch (action.type) {
        case VPPActionTypes.TOKEN_REQUEST:
            return {
                ...state,
                loading: true,
            };
        case VPPActionTypes.TOKEN_SUCCESS:
            if (isJSONAPIErrorResponsePayload(action.payload)) {
                return state;
            } else {
                return {
                    ...state,
                    data: action.payload,
                    loading: false,
                };
            }
        case VPPActionTypes.TOKEN_FAILURE:
            return {
                ...state,
                error: true,
            };
        default:
            return state;
    }
}
