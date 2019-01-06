import {MDMCertActionTypes} from "./mdmcert_actions";
import {CsrActionResponse, IMDMCertResponse} from "./mdmcert_actions";
import {isApiError} from "../../guards";
import {isJSONAPIErrorResponsePayload} from "../json-api";

export interface APNSState {
    data?: any;
    registeredEmail: string;
    csrLoading: boolean;
    csrResult?: IMDMCertResponse;
    error?: any;
}

const initialState: APNSState = {
    csrLoading: false,
    registeredEmail: "",
};

type APNSAction = CsrActionResponse;

export function apns(state: APNSState = initialState, action: APNSAction): APNSState {
    switch (action.type) {
        case MDMCertActionTypes.MDMCERT_CSR_REQUEST:
            return {
                ...state,
                csrLoading: true,
                csrResult: null,
                error: null,
            };
        case MDMCertActionTypes.MDMCERT_CSR_SUCCESS:
            if (isApiError(action.payload)) {
                return {
                    ...state,
                    csrLoading: false,
                    error: action.payload,
                }
            } else {
                return {
                    ...state,
                    csrLoading: false,
                    csrResult: action.payload,
                };
            }

        case MDMCertActionTypes.MDMCERT_CSR_FAILURE:
            return {
                ...state,
                csrLoading: false,
                error: action.payload,
            };
        default:
            return state;
    }
}
