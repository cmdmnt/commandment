import {Action, Dispatch} from "redux";
import {ApiError, RSAA, RSAAction} from "redux-api-middleware";
import {ThunkAction} from "redux-thunk";
import {RootState} from "../../reducers";
import {JSON_HEADERS} from "../constants";
import {JSONAPIDetailResponse, RSAAReadActionRequest, RSAAReadActionResponse} from "../json-api";

export enum MDMCertActionTypes {
     MDMCERT_CSR_REQUEST = "mdmcert/CSR_REQUEST",
     MDMCERT_CSR_SUCCESS = "mdmcert/CSR_SUCCESS",
     MDMCERT_CSR_FAILURE = "mdmcert/CSR_FAILURE",
     UPLOAD_CRYPTED_REQUEST = "mdmcert/UPLOAD_CRYPTED_REQUEST",
     UPLOAD_CRYPTED_SUCCESS = "mdmcert/UPLOAD_CRYPTED_SUCCESS",
     UPLOAD_CRYPTED_FAILURE = "mdmcert/UPLOAD_CRYPTED_FAILURE",
}

export interface IMDMCertResponse {
    result: "failure" | "success";
    reason?: string;
}

export type CsrActionRequest = (email: string) => RSAAction<
    MDMCertActionTypes.MDMCERT_CSR_REQUEST,
    MDMCertActionTypes.MDMCERT_CSR_SUCCESS,
    MDMCertActionTypes.MDMCERT_CSR_FAILURE>;

export interface CsrActionResponse {
    type: MDMCertActionTypes.MDMCERT_CSR_REQUEST |
          MDMCertActionTypes.MDMCERT_CSR_SUCCESS |
          MDMCertActionTypes.MDMCERT_CSR_FAILURE;
    payload?: ApiError | IMDMCertResponse;
}

export const csr: CsrActionRequest = (email: string) => {
    return {
        [RSAA]: {
            endpoint: `/api/v1/mdmcert/request/${email}`,
            headers: JSON_HEADERS,
            method: "GET",
            types: [
                MDMCertActionTypes.MDMCERT_CSR_REQUEST,
                MDMCertActionTypes.MDMCERT_CSR_SUCCESS,
                MDMCertActionTypes.MDMCERT_CSR_FAILURE,
            ],
        },
    };
};

export type UploadCryptedActionRequest = (file: File) => ThunkAction<void, RootState, void, UploadCryptedActionResponse>;
export type UploadCryptedActionResponse = RSAAReadActionResponse<
    MDMCertActionTypes.UPLOAD_CRYPTED_REQUEST,
    MDMCertActionTypes.UPLOAD_CRYPTED_SUCCESS,
    MDMCertActionTypes.UPLOAD_CRYPTED_FAILURE,
    JSONAPIDetailResponse<any, undefined>>;

export const uploadCrypted: UploadCryptedActionRequest = (file) => (
    dispatch: Dispatch,
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
                MDMCertActionTypes.UPLOAD_CRYPTED_REQUEST,
                MDMCertActionTypes.UPLOAD_CRYPTED_SUCCESS,
                MDMCertActionTypes.UPLOAD_CRYPTED_FAILURE,
            ],
        },
    });
};
