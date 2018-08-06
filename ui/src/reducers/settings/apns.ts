import * as actions from "../../actions/settings/mdmcert";
import {isJSONAPIErrorResponsePayload} from "../../json-api";
import {CsrActionResponse, IMDMCertResponse} from "../../actions/settings/mdmcert";
import {isApiError} from "../../guards";

export interface APNSState {
    data?: any;
    registeredEmail: string;
    csrLoading: boolean;
    csrResult?: IMDMCertResponse;
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
                csrLoading: true,
                error: null,
                csrResult: null,
            };
        case actions.MDMCERT_CSR_SUCCESS:
            if (isApiError(action.payload)) {
                return {
                    ...state,
                    csrLoading: false,
                    error: action.payload
                }
            } else {
                return {
                    ...state,
                    csrResult: action.payload,
                    csrLoading: false
                };
            }

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
