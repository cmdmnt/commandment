import {AuthenticationActions, AuthenticationActionTypes} from "./actions";
import {isApiError} from "../../guards";
import {ApiError} from "redux-api-middleware";

export interface IAuthenticationState {
    // In reality, nobody should store the secret client side, but we need to establish an authentication system before
    // returning to using a more secure method.
    oauth2_client_id: string;
    oauth2_client_secret: string;

    access_token?: string;
    expires_in?: number;
    token_type?: string;

    loading: boolean;

    error?: ApiError;
}

const initialState: IAuthenticationState = {
    access_token: sessionStorage.getItem("cmdmnt-token"),
    error: null,
    expires_in: 0,
    loading: false,
    oauth2_client_id: "F8955645-A21D-44AE-9387-42B0800ADF15",
    oauth2_client_secret: "dummyvalue",
    token_type: null,
};

export function reducer(state: IAuthenticationState = initialState, action: AuthenticationActions) {
    switch (action.type) {
        case AuthenticationActionTypes.TOKEN_REQUEST:
            return {
                ...state,
                loading: true,
            };
        case AuthenticationActionTypes.TOKEN_SUCCESS:
            return {
                ...state,
                access_token: action.payload.access_token,
                expires_in: action.payload.expires_in,
                loading: false,
                token_type: action.payload.token_type,
            };
        case AuthenticationActionTypes.TOKEN_FAILURE:
            let err = null;

            if (isApiError(action.payload)) {
                err = action.payload;
            }
            return {
                ...state,
                error: err,
                loading: false,
            };
        case AuthenticationActionTypes.TOKEN_SAVE:
            return state;
        default:
            return state;
    }
}
