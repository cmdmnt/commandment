import {IVPPAction, TokenActionResponse, VPPActionTypes} from "../../actions/vpp";
import {VPPAccount} from "../../models";

export interface VPPState {
    data?: VPPAccount;
    loading: boolean;
    submitted: boolean;
    error: boolean;
    errorDetail?: any;
}

const initialState: VPPState = {
    loading: false,
    error: false,
    submitted: false
};

type VPPAction = TokenActionResponse;

export function vpp(state: VPPState = initialState, action: VPPAction): VPPState {
    switch (action.type) {
        case VPPActionTypes.TOKEN_REQUEST:
            return {
                ...state,
                loading: true
            };
        case VPPActionTypes.TOKEN_SUCCESS:
            return {
                ...state,
                loading: false,
                data: action.payload
            };
        case VPPActionTypes.TOKEN_FAILURE:
            return {
                ...state,
                error: true
            };
        default:
            return state;
    }
}