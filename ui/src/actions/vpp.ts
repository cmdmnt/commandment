import {JSONAPIDetailResponse, RSAAReadActionRequest, RSAAReadActionResponse} from "../json-api";
import {VPPAccount} from "../models";
import {RSAA, RSAAction} from "redux-api-middleware";
import {JSON_HEADERS} from "./constants";
import {ThunkAction} from "redux-thunk";
import {IRootState} from "../reducers/index";
import {Dispatch} from "react-redux";

export const TOKEN_REQUEST = 'vpp/TOKEN_REQUEST';
export type TOKEN_REQUEST = typeof TOKEN_REQUEST;
export const TOKEN_SUCCESS = 'vpp/TOKEN_SUCCESS';
export type TOKEN_SUCCESS = typeof TOKEN_SUCCESS;
export const TOKEN_FAILURE = 'vpp/TOKEN_FAILURE';
export type TOKEN_FAILURE = typeof TOKEN_FAILURE;

export type TokenActionRequest = RSAAReadActionRequest<TOKEN_REQUEST, TOKEN_SUCCESS, TOKEN_FAILURE>;
export type TokenActionResponse = RSAAReadActionResponse<TOKEN_REQUEST, TOKEN_SUCCESS, TOKEN_FAILURE, VPPAccount>;

export const read: TokenActionRequest = (id: string) => {
    return (<RSAAction<TOKEN_REQUEST, TOKEN_SUCCESS, TOKEN_FAILURE>>{
        [RSAA]: {
            endpoint: '/api/v1/vpp/token',
            method: 'GET',
            types: [
                TOKEN_REQUEST, TOKEN_SUCCESS, TOKEN_FAILURE
            ],
            headers: JSON_HEADERS
        }
    });
};

export const UPLOAD_TOKEN = 'vpp/UPLOAD_TOKEN';
export type UPLOAD_TOKEN = typeof UPLOAD_TOKEN;

export const UPLOAD_REQUEST = 'vpp/UPLOAD_REQUEST';
export type UPLOAD_REQUEST = typeof UPLOAD_REQUEST;
export const UPLOAD_SUCCESS = 'vpp/UPLOAD_SUCCESS';
export type UPLOAD_SUCCESS = typeof UPLOAD_SUCCESS;
export const UPLOAD_FAILURE = 'vpp/UPLOAD_FAILURE';
export type UPLOAD_FAILURE = typeof UPLOAD_FAILURE;

export interface UploadActionRequest {
    (file: File): ThunkAction<void, IRootState, void>;
}
export type UploadActionResponse = RSAAReadActionResponse<UPLOAD_REQUEST, UPLOAD_SUCCESS, UPLOAD_FAILURE, JSONAPIDetailResponse<VPPAccount, undefined>>;

export const upload = (file: File): ThunkAction<void, IRootState, void> => (
    dispatch: Dispatch<IRootState>,
    getState: () => IRootState,
    extraArgument: void) => {

    const data = new FormData();
    data.append('file', file);
    dispatch({
        type: UPLOAD_TOKEN,
        payload: data
    });

    dispatch({
        [RSAA]: {
            endpoint: `/api/v1/vpp/upload/token`,
            method: 'POST',
            types: [
                UPLOAD_REQUEST,
                UPLOAD_SUCCESS,
                UPLOAD_FAILURE
            ],
            body: data
        }
    })
};