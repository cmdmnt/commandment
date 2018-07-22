import {JSONAPIDetailResponse, RSAAReadActionRequest, RSAAReadActionResponse} from "../../json-api";
import {ApiError, RSAA, RSAAction} from "redux-api-middleware";
import {JSON_HEADERS} from "../constants";

export const MDMCERT_CSR_REQUEST = "mdmcert/CSR_REQUEST";
export type MDMCERT_CSR_REQUEST = typeof MDMCERT_CSR_REQUEST;
export const MDMCERT_CSR_SUCCESS = "mdmcert/CSR_SUCCESS";
export type MDMCERT_CSR_SUCCESS = typeof MDMCERT_CSR_SUCCESS;
export const MDMCERT_CSR_FAILURE = "mdmcert/CSR_FAILURE";
export type MDMCERT_CSR_FAILURE = typeof MDMCERT_CSR_FAILURE;

export interface IMDMCertResponse {
    result: 'failure' | 'succcess';
    reason?: string;
}

type CsrActionRequest = (email: string) => RSAAction<MDMCERT_CSR_REQUEST, MDMCERT_CSR_SUCCESS, MDMCERT_CSR_FAILURE>;
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
            headers: JSON_HEADERS
        },
    };
};


