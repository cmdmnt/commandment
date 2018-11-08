import * as actions from '../../actions/certificates/ssl';
import {JSONAPIListResponse, JSONAPIDataObject} from "../../json-api";
import {Certificate} from "../../models";

export interface SSLState {
    items?: JSONAPIListResponse<JSONAPIDataObject<Certificate>>;
    loading: boolean;
    error: boolean;
    errorDetail?: any
    lastReceived?: Date;
}

const initialState: SSLState = {
    loading: false,
    error: false,
    errorDetail: null,
    lastReceived: null
};

export type PushAction = actions.FetchSSLCertificatesActionResponse;

export function ssl(state: SSLState = initialState, action: PushAction): SSLState {
    switch (action.type) {
        case actions.SSLCERT_REQUEST:
            return {
                ...state,
                loading: true
            };
        case actions.SSLCERT_FAILURE:
            return {
                ...state,
                loading: false,
                error: true,
                errorDetail: action.payload
            };
        case actions.SSLCERT_SUCCESS:
            return {
                ...state,
                items: action.payload,
                lastReceived: new Date(),
                error: false,
                errorDetail: null
            };
        default:
            return state;
    }
}