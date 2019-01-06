import { RSAA, RSAAction } from "redux-api-middleware";
import { JSONAPI_HEADERS } from "../constants"
import {CertificatePurpose} from "./types";

export type NEW_REQUEST = "signing_requests/NEW_REQUEST";
export const NEW_REQUEST: NEW_REQUEST = "signing_requests/NEW_REQUEST";
export type NEW_SUCCESS = "signing_requests/NEW_SUCCESS";
export const NEW_SUCCESS: NEW_SUCCESS = "signing_requests/NEW_SUCCESS";
export type NEW_FAILURE = "signing_requests/NEW_FAILURE";
export const NEW_FAILURE: NEW_FAILURE = "signing_requests/NEW_FAILURE";

export const newCertificateSigningRequest = (purpose: CertificatePurpose): RSAAction<NEW_REQUEST, NEW_SUCCESS, NEW_FAILURE>  => {
    return {
        [RSAA]: {
            body: JSON.stringify({ purpose }),
            endpoint: "/api/v1/certificate_signing_requests/new",
            headers: JSONAPI_HEADERS,
            method: "GET",
            types: [
                NEW_REQUEST,
                NEW_SUCCESS,
                NEW_FAILURE,
            ],
        },
    }
};
