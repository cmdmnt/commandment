import {RSAAReadActionRequest, RSAAReadActionResponse} from "../json-api";
import {VPPAccount} from "../models";
import {CALL_API, RSAA} from "redux-api-middleware";
import {JSON_HEADERS} from "./constants";

export const TOKEN_REQUEST = 'vpp/TOKEN_REQUEST';
export type TOKEN_REQUEST = typeof TOKEN_REQUEST;
export const TOKEN_SUCCESS = 'vpp/TOKEN_SUCCESS';
export type TOKEN_SUCCESS = typeof TOKEN_SUCCESS;
export const TOKEN_FAILURE = 'vpp/TOKEN_FAILURE';
export type TOKEN_FAILURE = typeof TOKEN_FAILURE;

export type TokenActionRequest = RSAAReadActionRequest<TOKEN_REQUEST, TOKEN_SUCCESS, TOKEN_FAILURE>;
export type TokenActionResponse = RSAAReadActionResponse<TOKEN_REQUEST, TOKEN_SUCCESS, TOKEN_FAILURE, VPPAccount>;

export const read: TokenActionRequest = (id: string) => {
    return (<RSAA<TOKEN_REQUEST, TOKEN_SUCCESS, TOKEN_FAILURE>>{
        [CALL_API]: {
            endpoint: '/api/v1/vpp/token',
            method: 'GET',
            types: [
                TOKEN_REQUEST, TOKEN_SUCCESS, TOKEN_FAILURE
            ],
            headers: JSON_HEADERS
        }
    });
};
