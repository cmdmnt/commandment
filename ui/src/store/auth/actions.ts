import { RSAA, RSAAction } from "redux-api-middleware";
import {JSONAPI_HEADERS} from "../constants";
import {IOAuth2TokenSuccessResponse} from "./types";

export enum AuthenticationActionTypes {
    TOKEN_REQUEST = "authentication/TOKEN_REQUEST",
    TOKEN_SUCCESS = "authentication/TOKEN_SUCCESS",
    TOKEN_FAILURE = "authentication/TOKEN_FAILURE",
}

export type TokenActionRequest = (email: string, password: string) => RSAAction<
    AuthenticationActionTypes.TOKEN_REQUEST,
    AuthenticationActionTypes.TOKEN_SUCCESS,
    AuthenticationActionTypes.TOKEN_FAILURE>;

export interface TokenActionResponse {
    type: AuthenticationActionTypes.TOKEN_REQUEST |
          AuthenticationActionTypes.TOKEN_SUCCESS |
          AuthenticationActionTypes.TOKEN_FAILURE;
    payload?: IOAuth2TokenSuccessResponse;
}

export const login: TokenActionRequest = (email: string, password: string) => {
    const queryParameters: string[] = ["grant_type=password", "response_type=token",
        "client_id=F8955645-A21D-44AE-9387-42B0800ADF15", "client_secret=A"];
    const body: FormData = new FormData();
    body.append("username", email);
    body.append("password", password);

    return {
        [RSAA]: {
            body,
            endpoint: "/oauth/token?" + queryParameters.join("&"),
            headers: {
                "Accept": "application/json",
                "Authorization": "Basic Rjg5NTU2NDUtQTIxRC00NEFFLTkzODctNDJCMDgwMEFERjE1OkE=",
                // "Content-Type": "application/x-www-form-urlencoded",
            },
            method: "POST",
            types: [
                AuthenticationActionTypes.TOKEN_REQUEST,
                AuthenticationActionTypes.TOKEN_SUCCESS,
                AuthenticationActionTypes.TOKEN_FAILURE,
            ],
        },
    }
};

export type AuthenticationActions = TokenActionResponse;
