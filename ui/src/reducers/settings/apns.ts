import * as actions from "../../actions/settings/mdmcert";
import {isJSONAPIErrorResponsePayload} from "../../json-api";
import {CsrActionResponse} from "../../actions/settings/mdmcert";

export interface APNSState {
    data?: any;
    registeredEmail: string;
    csrLoading: boolean;
    error?: any;
}

const initialState: APNSState = {
    registeredEmail: "",
    csrLoading: false,
};

type APNSAction = CsrActionResponse;

export function apns(state: APNSState = initialState, action: APNSAction): APNSState {
    switch (action.type) {
        case actions.MDMCERT_CSR_REQUEST:
            return {
                ...state,
                csrLoading: true
            };
        case actions.MDMCERT_CSR_SUCCESS:
            return {
                ...state,
                csrLoading: false
            };
        case actions.MDMCERT_CSR_FAILURE:
            return {
                ...state,
                csrLoading: false,
                error: action.payload,
            };
        default:
            return state;
    }
}
