import {Dispatch} from "react-redux";
import {HTTPVerb, RSAA, RSAAction} from "redux-api-middleware";
import {ThunkAction} from "redux-thunk";
import {
    encodeJSONAPIIndexParameters,
    JSONAPIDetailResponse, RSAAIndexActionRequest,
    RSAAIndexActionResponse,
    RSAAReadActionRequest,
    RSAAReadActionResponse
} from "../../json-api";
import {VPPAccount} from "../../models";
import {RootState} from "../../reducers/index";
import {JSON_HEADERS, JSONAPI_HEADERS} from "../../actions/constants";

export enum VPPActionTypes {
    TOKEN_REQUEST = "vpp/TOKEN_REQUEST",
    TOKEN_SUCCESS = "vpp/TOKEN_SUCCESS",
    TOKEN_FAILURE = "vpp/TOKEN_FAILURE",
    UPLOAD_REQUEST = "vpp/UPLOAD_REQUEST",
    UPLOAD_SUCCESS = "vpp/UPLOAD_SUCCESS",
    UPLOAD_FAILURE = "vpp/UPLOAD_FAILURE",
    UPLOAD_TOKEN = "vpp/UPLOAD_TOKEN",
    INDEX_REQUEST = "vpp/INDEX_REQUEST",
    INDEX_SUCCESS = "vpp/INDEX_SUCCESS",
    INDEX_FAILURE = "vpp/INDEX_FAILURE",
}

export interface IVPPAction {
    type: VPPActionTypes;
}

export type TokenActionRequest = RSAAReadActionRequest<VPPActionTypes.TOKEN_REQUEST, VPPActionTypes.TOKEN_SUCCESS, VPPActionTypes.TOKEN_FAILURE>;
export type TokenActionResponse = RSAAReadActionResponse<VPPActionTypes.TOKEN_REQUEST, VPPActionTypes.TOKEN_SUCCESS, VPPActionTypes.TOKEN_FAILURE, VPPAccount>;

export const read: TokenActionRequest = (id: string) => {
    return ({
        [RSAA]: {
            endpoint: "/api/v1/vpp/token",
            headers: JSON_HEADERS,
            method: "GET",
            types: [
                VPPActionTypes.TOKEN_REQUEST,
                VPPActionTypes.TOKEN_SUCCESS,
                VPPActionTypes.TOKEN_FAILURE,
            ],
        },
    } as RSAAction<VPPActionTypes.TOKEN_REQUEST, VPPActionTypes.TOKEN_SUCCESS, VPPActionTypes.TOKEN_FAILURE>);
};

export type UploadActionRequest = (file: File) => ThunkAction<void, RootState, void>;
export type UploadActionResponse = RSAAReadActionResponse<VPPActionTypes.UPLOAD_REQUEST, VPPActionTypes.UPLOAD_SUCCESS, VPPActionTypes.UPLOAD_FAILURE,
    JSONAPIDetailResponse<VPPAccount, undefined>>;

export const upload = (file: File): ThunkAction<void, RootState, void> => (
    dispatch: Dispatch<RootState>,
    getState: () => RootState,
    extraArgument: void) => {

    const data = new FormData();
    data.append("file", file);
    dispatch({
        payload: data,
        type: VPPActionTypes.UPLOAD_TOKEN,
    });

    dispatch({
        [RSAA]: {
            body: data,
            endpoint: `/api/v1/vpp/upload/token`,
            method: "POST",
            types: [
                VPPActionTypes.UPLOAD_REQUEST,
                VPPActionTypes.UPLOAD_SUCCESS,
                VPPActionTypes.UPLOAD_FAILURE,
            ],
        },
    });
};

export type IndexActionRequest = RSAAIndexActionRequest<VPPActionTypes.INDEX_REQUEST, VPPActionTypes.INDEX_SUCCESS, VPPActionTypes.INDEX_FAILURE>;
export type IndexActionResponse = RSAAIndexActionResponse<VPPActionTypes.INDEX_REQUEST, VPPActionTypes.INDEX_SUCCESS, VPPActionTypes.INDEX_FAILURE, VPPAccount>;

export const index = encodeJSONAPIIndexParameters((queryParameters: string[]) => {
    return (<RSAAction<VPPActionTypes.INDEX_REQUEST, VPPActionTypes.INDEX_SUCCESS, VPPActionTypes.INDEX_FAILURE>>{
        [RSAA]: {
            endpoint: '/api/v1/vpp_accounts?' + queryParameters.join('&'),
            method: (<HTTPVerb>'GET'),
            types: [
                VPPActionTypes.INDEX_REQUEST,
                VPPActionTypes.INDEX_SUCCESS,
                VPPActionTypes.INDEX_FAILURE
            ],
            headers: JSONAPI_HEADERS
        }
    });
});

