import {ICsrActionResponse, MDMCertActionTypes, UploadCryptedActionResponse} from "./mdmcert_actions";
import {IMDMCertResponse} from "./types";
import {isApiError} from "../../guards";
import {ApiError} from "redux-api-middleware";

export interface APNSState {
    csrError: ApiError<any>;
    csrLoading: boolean;
    csrResult: IMDMCertResponse;
    data?: any;
    decryptError: ApiError<any>;
    decryptLoading: boolean;
    registeredEmail: string;
}

const initialState: APNSState = {
    csrError: null,
    csrLoading: false,
    csrResult: null,
    decryptError: null,
    decryptLoading: false,
    registeredEmail: "",
};

type APNSAction = ICsrActionResponse | UploadCryptedActionResponse;

export function apns(state: APNSState = initialState, action: APNSAction): APNSState {
    switch (action.type) {
        case MDMCertActionTypes.MDMCERT_CSR_REQUEST:
            return {
                ...state,
                csrError: null,
                csrLoading: true,
                csrResult: null,
            };
        case MDMCertActionTypes.MDMCERT_CSR_SUCCESS:
            if (isApiError(action.payload)) {
                return {
                    ...state,
                    csrError: action.payload,
                    csrLoading: false,
                }
            } else {
                return {
                    ...state,
                    csrError: null,
                    csrLoading: false,
                    csrResult: action.payload,
                };
            }
        case MDMCertActionTypes.MDMCERT_CSR_FAILURE:
            return {
                ...state,
                csrError: action.payload,
                csrLoading: false,
            };
        case MDMCertActionTypes.UPLOAD_CRYPTED_REQUEST:
            return {
                ...state,
                decryptError: null,
                decryptLoading: true,
            };
        case MDMCertActionTypes.UPLOAD_CRYPTED_FAILURE:
            return {
                ...state,
                decryptError: action.payload,
                decryptLoading: false,
            };
        case MDMCertActionTypes.UPLOAD_CRYPTED_SUCCESS:
            return {
                ...state,
                decryptError: null,
                decryptLoading: false,
            };
        default:
            return state;
    }
}
