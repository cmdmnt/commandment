import {JSONAPIDataObject, JSONAPIListResponse} from "../../json-api";
import * as actions from "./ssl_actions";
import {Certificate} from "./types";

export interface SSLState {
    items?: JSONAPIListResponse<JSONAPIDataObject<Certificate>>;
    loading: boolean;
    error: boolean;
    errorDetail?: any
    lastReceived?: Date;
}

const initialState: SSLState = {
    error: false,
    errorDetail: null,
    lastReceived: null,
    loading: false,
};

export type PushAction = actions.FetchSSLCertificatesActionResponse;

export function ssl(state: SSLState = initialState, action: PushAction): SSLState {
    switch (action.type) {
        case actions.SSLCERT_REQUEST:
            return {
                ...state,
                loading: true,
            };
        case actions.SSLCERT_FAILURE:
            return {
                ...state,
                error: true,
                errorDetail: action.payload,
                loading: false,
            };
        case actions.SSLCERT_SUCCESS:
            return {
                ...state,
                error: false,
                errorDetail: null,
                items: action.payload,
                lastReceived: new Date(),
            };
        default:
            return state;
    }
}
