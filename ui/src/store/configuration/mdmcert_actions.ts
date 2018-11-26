import {Dispatch} from "react-redux";
import {ApiError, RSAA, RSAAction} from "redux-api-middleware";
import {ThunkAction} from "redux-thunk";
import {JSON_HEADERS} from "../../actions/constants";
import {JSONAPIDetailResponse, RSAAReadActionRequest, RSAAReadActionResponse} from "../../json-api";
import {VPPAccount} from "../../models";
import {RootState} from "../../reducers/index";
import {UPLOAD_TOKEN} from "./vpp";

export const MDMCERT_CSR_REQUEST = "mdmcert/CSR_REQUEST";
export type MDMCERT_CSR_REQUEST = typeof MDMCERT_CSR_REQUEST;
export const MDMCERT_CSR_SUCCESS = "mdmcert/CSR_SUCCESS";
export type MDMCERT_CSR_SUCCESS = typeof MDMCERT_CSR_SUCCESS;
export const MDMCERT_CSR_FAILURE = "mdmcert/CSR_FAILURE";
export type MDMCERT_CSR_FAILURE = typeof MDMCERT_CSR_FAILURE;

export interface IMDMCertResponse {
    result: "failure" | "success";
    reason?: string;
}

export type CsrActionRequest = (email: string) => RSAAction<MDMCERT_CSR_REQUEST, MDMCERT_CSR_SUCCESS, MDMCERT_CSR_FAILURE>;
export interface CsrActionResponse {
    type: MDMCERT_CSR_REQUEST | MDMCERT_CSR_SUCCESS | MDMCERT_CSR_FAILURE;
    payload?: ApiError | IMDMCertResponse;
}

export const csr: CsrActionRequest = (email: string) => {
    return {
        [RSAA]: {
            endpoint: `/api/v1/mdmcert/request/${email}`,
            method: "GET",
            types: [
                MDMCERT_CSR_REQUEST,
                MDMCERT_CSR_SUCCESS,
                MDMCERT_CSR_FAILURE,
            ],
            headers: JSON_HEADERS,
        },
    };
};

export const UPLOAD_CRYPTED_REQUEST = "mdmcert/UPLOAD_CRYPTED_REQUEST";
export type UPLOAD_CRYPTED_REQUEST = typeof UPLOAD_CRYPTED_REQUEST;
export const UPLOAD_CRYPTED_SUCCESS = "mdmcert/UPLOAD_CRYPTED_SUCCESS";
export type UPLOAD_CRYPTED_SUCCESS = typeof UPLOAD_CRYPTED_SUCCESS;
export const UPLOAD_CRYPTED_FAILURE = "mdmcert/UPLOAD_CRYPTED_FAILURE";
export type UPLOAD_CRYPTED_FAILURE = typeof UPLOAD_CRYPTED_FAILURE;

export type UploadCryptedActionRequest = (file: File) => ThunkAction<void, RootState, void>;
export type UploadCryptedActionResponse = RSAAReadActionResponse<UPLOAD_CRYPTED_REQUEST, UPLOAD_CRYPTED_SUCCESS, UPLOAD_CRYPTED_FAILURE,
    JSONAPIDetailResponse<any, undefined>>;

export const uploadCrypted: UploadCryptedActionRequest = (file) => (
    dispatch: Dispatch<RootState>,
    getState: () => RootState,
    extraArgument: void) => {

    const data = new FormData();
    data.append("file", file);
    // dispatch({
    //     payload: data,
    //     type: UPLOAD_TOKEN,
    // });

    dispatch({
        [RSAA]: {
            body: data,
            endpoint: `/api/v1/mdmcert/decrypt`,
            method: "POST",
            types: [
                UPLOAD_CRYPTED_REQUEST,
                UPLOAD_CRYPTED_SUCCESS,
                UPLOAD_CRYPTED_FAILURE,
            ],
        },
    });
};
