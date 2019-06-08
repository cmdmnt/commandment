import { RSAA, RSAAction } from "redux-api-middleware";
import {JSONAPI_HEADERS, OAUTH2_CLIENT_ID, OAUTH2_CLIENT_SECRET} from "../constants";
import {IOAuth2TokenSuccessResponse} from "./types";
import {ThunkAction} from "redux-thunk";
import {RootState} from "../../reducers";
import {Action, ActionCreator} from "redux";

export enum AuthenticationActionTypes {
    TOKEN_REQUEST = "authentication/TOKEN_REQUEST",
    TOKEN_SUCCESS = "authentication/TOKEN_SUCCESS",
    TOKEN_FAILURE = "authentication/TOKEN_FAILURE",

    TOKEN_SAVE = "authentication/TOKEN_SAVE",
}

export type TokenActionRequest = RSAAction<
    AuthenticationActionTypes.TOKEN_REQUEST,
    AuthenticationActionTypes.TOKEN_SUCCESS,
    AuthenticationActionTypes.TOKEN_FAILURE>;

export type TokenActionRequestCreator = (email: string, password: string) => TokenActionRequest;

export interface ITokenActionResponse {
    type: AuthenticationActionTypes.TOKEN_REQUEST |
          AuthenticationActionTypes.TOKEN_SUCCESS |
          AuthenticationActionTypes.TOKEN_FAILURE;
    payload?: IOAuth2TokenSuccessResponse;
}

export const createToken: TokenActionRequestCreator = (email: string, password: string) => {
    const queryParameters: string[] = ["grant_type=password", "response_type=token"];
        // ,"client_id=F8955645-A21D-44AE-9387-42B0800ADF15", "client_secret=A"];
    const body: FormData = new FormData();
    // body.append("grant_type", "password");
    body.append("username", email);
    body.append("password", password);

    return {
        [RSAA]: {
            body,
            endpoint: "/oauth/token?" + queryParameters.join("&"),
            headers: {
                Accept: "application/json",
                Authorization: "Basic " + btoa(OAUTH2_CLIENT_ID + ":" + OAUTH2_CLIENT_SECRET),
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

export interface ITokenSaveRequest extends Action<AuthenticationActionTypes.TOKEN_SAVE> {
    token: string;
}

export const saveToken: ActionCreator<ITokenSaveRequest> = (payload) => {
    sessionStorage.setItem("cmdmnt-token", payload.access_token);

    return {
        ...payload,
        type: AuthenticationActionTypes.TOKEN_SAVE,
    };
};

export const login = (email: string, password: string): ThunkAction<void, RootState, null, TokenActionRequest> =>
    (dispatch, getState) => {

    return dispatch(createToken(email, password)).then((res) => {
        console.log(res);
        dispatch(saveToken(res.payload));
    }).then(() => {
        console.log("saved token");
    })
};

export type AuthenticationActions = ITokenActionResponse | Action<AuthenticationActionTypes.TOKEN_SAVE>;
