import {
    encodeJSONAPIIndexParameters,
    RSAAIndexActionRequest,
    RSAAIndexActionResponse,
    RSAAReadActionRequest, RSAAReadActionResponse
} from "../../json-api";
import {DEPAccount} from "../../models";
import {HTTPVerb, RSAA, RSAAction} from "redux-api-middleware";
import {JSONAPI_HEADERS} from "../constants";

export enum DEPActionTypes {
    INDEX_REQUEST = "dep/INDEX_REQUEST",
    INDEX_SUCCESS = "dep/INDEX_SUCCESS",
    INDEX_FAILURE = "dep/INDEX_FAILURE",

    ACCT_READ_REQUEST = "dep/account/READ_REQUEST",
    ACCT_READ_SUCCESS = "dep/account/READ_SUCCESS",
    ACCT_READ_FAILURE = "dep/account/READ_FAILURE",
}

export type IndexActionRequest = RSAAIndexActionRequest<DEPActionTypes.INDEX_REQUEST, DEPActionTypes.INDEX_SUCCESS, DEPActionTypes.INDEX_FAILURE>;
export type IndexActionResponse = RSAAIndexActionResponse<DEPActionTypes.INDEX_REQUEST, DEPActionTypes.INDEX_SUCCESS, DEPActionTypes.INDEX_FAILURE, DEPAccount>;

export const index = encodeJSONAPIIndexParameters((queryParameters: string[]) => {
    return (<RSAAction<DEPActionTypes.INDEX_REQUEST, DEPActionTypes.INDEX_SUCCESS, DEPActionTypes.INDEX_FAILURE>>{
        [RSAA]: {
            endpoint: '/api/v1/dep/accounts?' + queryParameters.join('&'),
            method: (<HTTPVerb>'GET'),
            types: [
                DEPActionTypes.INDEX_REQUEST,
                DEPActionTypes.INDEX_SUCCESS,
                DEPActionTypes.INDEX_FAILURE
            ],
            headers: JSONAPI_HEADERS
        }
    });
});


export type ReadActionRequest = RSAAReadActionRequest<DEPActionTypes.ACCT_READ_REQUEST, DEPActionTypes.ACCT_READ_SUCCESS, DEPActionTypes.ACCT_READ_FAILURE>;
export type ReadActionResponse = RSAAReadActionResponse<DEPActionTypes.ACCT_READ_REQUEST, DEPActionTypes.ACCT_READ_SUCCESS, DEPActionTypes.ACCT_READ_FAILURE, DEPAccount>;

export const read: ReadActionRequest = (id: string, include?: Array<string>) => {

    let inclusions = '';
    if (include && include.length) {
        inclusions = 'include=' + include.join(',')
    }

    return {
        [RSAA]: {
            endpoint: `/api/v1/dep/accounts/${id}?${inclusions}`,
            method: 'GET',
            types: [
                DEPActionTypes.ACCT_READ_REQUEST,
                DEPActionTypes.ACCT_READ_SUCCESS,
                DEPActionTypes.ACCT_READ_FAILURE
            ],
            headers: JSONAPI_HEADERS
        }
    }
};

export type DEPActions = IndexActionResponse & ReadActionResponse;

