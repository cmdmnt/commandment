import {AuthenticationActions} from "./actions";

export interface IAuthenticationState {
    // In reality, nobody should store the secret client side, but we need to establish an authentication system before
    // returning to using a more secure method.
    oauth2_client_id: string;
    oauth2_client_secret: string;

    access_token?: string;
    expires_in?: number;
    token_type?: string;
}

const initialState: IAuthenticationState = {
    oauth2_client_id: "F8955645-A21D-44AE-9387-42B0800ADF15",
    oauth2_client_secret: "dummyvalue",

    access_token: null,
    expires_in: 0,
    token_type: null,
};

export function reducer(state: IAuthenticationState = initialState, action: AuthenticationActions) {
    switch (action.type) {
        default:
            return state;
    }
}
