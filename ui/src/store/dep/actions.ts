import {
    encodeJSONAPIChildIndexParameters,
    encodeJSONAPIIndexParameters,
    RSAAIndexActionRequest,
    RSAAIndexActionResponse,
    RSAAReadActionRequest, RSAAReadActionResponse
} from "../../json-api";
import {DEPAccount, DEPProfile} from "./types";
import {HTTPVerb, RSAA, RSAAction} from "redux-api-middleware";
import {JSONAPI_HEADERS} from "../../actions/constants";


export enum DEPActionTypes {
    ACCT_INDEX_REQUEST = "dep/account/INDEX_REQUEST",
    ACCT_INDEX_SUCCESS = "dep/account/INDEX_SUCCESS",
    ACCT_INDEX_FAILURE = "dep/account/INDEX_FAILURE",

    ACCT_READ_REQUEST = "dep/account/READ_REQUEST",
    ACCT_READ_SUCCESS = "dep/account/READ_SUCCESS",
    ACCT_READ_FAILURE = "dep/account/READ_FAILURE",

    PROF_INDEX_REQUEST = "dep/profile/INDEX_REQUEST",
    PROF_INDEX_SUCCESS = "dep/profile/INDEX_SUCCESS",
    PROF_INDEX_FAILURE = "dep/profile/INDEX_FAILURE",

    PROF_READ_REQUEST = "dep/profile/READ_REQUEST",
    PROF_READ_SUCCESS = "dep/profile/READ_SUCCESS",
    PROF_READ_FAILURE = "dep/profile/READ_FAILURE",
}

export type AccountIndexActionRequest = RSAAIndexActionRequest<DEPActionTypes.ACCT_INDEX_REQUEST, DEPActionTypes.ACCT_INDEX_SUCCESS, DEPActionTypes.ACCT_INDEX_FAILURE>;
export type AccountIndexActionResponse = RSAAIndexActionResponse<DEPActionTypes.ACCT_INDEX_REQUEST, DEPActionTypes.ACCT_INDEX_SUCCESS, DEPActionTypes.ACCT_INDEX_FAILURE, DEPAccount>;

export const accounts = encodeJSONAPIIndexParameters((queryParameters: string[]) => {
    return (<RSAAction<DEPActionTypes.ACCT_INDEX_REQUEST, DEPActionTypes.ACCT_INDEX_SUCCESS, DEPActionTypes.ACCT_INDEX_FAILURE>>{
        [RSAA]: {
            endpoint: '/api/v1/dep/accounts?' + queryParameters.join('&'),
            method: (<HTTPVerb>'GET'),
            types: [
                DEPActionTypes.ACCT_INDEX_REQUEST,
                DEPActionTypes.ACCT_INDEX_SUCCESS,
                DEPActionTypes.ACCT_INDEX_FAILURE
            ],
            headers: JSONAPI_HEADERS
        }
    });
});


export type AccountReadActionRequest = RSAAReadActionRequest<DEPActionTypes.ACCT_READ_REQUEST, DEPActionTypes.ACCT_READ_SUCCESS, DEPActionTypes.ACCT_READ_FAILURE>;
export type AccountReadActionResponse = RSAAReadActionResponse<DEPActionTypes.ACCT_READ_REQUEST, DEPActionTypes.ACCT_READ_SUCCESS, DEPActionTypes.ACCT_READ_FAILURE, DEPAccount>;

export const account: AccountReadActionRequest = (id: string, include?: Array<string>) => {

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

export type ProfileIndexActionRequest = RSAAIndexActionRequest<DEPActionTypes.PROF_INDEX_REQUEST, DEPActionTypes.PROF_INDEX_SUCCESS, DEPActionTypes.PROF_INDEX_FAILURE>;
export type ProfileIndexActionResponse = RSAAIndexActionResponse<DEPActionTypes.PROF_INDEX_REQUEST, DEPActionTypes.PROF_INDEX_SUCCESS, DEPActionTypes.PROF_INDEX_FAILURE, DEPProfile>;

export const profiles = encodeJSONAPIChildIndexParameters((dep_account_id: string, queryParameters: string[]) => {
    return (<RSAAction<DEPActionTypes.PROF_INDEX_REQUEST, DEPActionTypes.PROF_INDEX_SUCCESS, DEPActionTypes.PROF_INDEX_FAILURE>>{
        [RSAA]: {
            endpoint: `/api/v1/dep/accounts/${dep_account_id}/profiles?` + queryParameters.join('&'),
            method: (<HTTPVerb>'GET'),
            types: [
                DEPActionTypes.PROF_INDEX_REQUEST,
                DEPActionTypes.PROF_INDEX_SUCCESS,
                DEPActionTypes.PROF_INDEX_FAILURE
            ],
            headers: JSONAPI_HEADERS
        }
    });
});

export type ProfileReadActionRequest = RSAAReadActionRequest<DEPActionTypes.PROF_READ_REQUEST, DEPActionTypes.PROF_READ_SUCCESS, DEPActionTypes.PROF_READ_FAILURE>;
export type ProfileReadActionResponse = RSAAReadActionResponse<DEPActionTypes.PROF_READ_REQUEST, DEPActionTypes.PROF_READ_SUCCESS, DEPActionTypes.PROF_READ_FAILURE, DEPProfile>;

export const profile: ProfileReadActionRequest = (id: string, include?: Array<string>) => {

    let inclusions = '';
    if (include && include.length) {
        inclusions = 'include=' + include.join(',')
    }

    return {
        [RSAA]: {
            endpoint: `/api/v1/dep/profiles/${id}?${inclusions}`,
            method: 'GET',
            types: [
                DEPActionTypes.PROF_READ_REQUEST,
                DEPActionTypes.PROF_READ_SUCCESS,
                DEPActionTypes.PROF_READ_FAILURE
            ],
            headers: JSONAPI_HEADERS
        }
    }
};

export type DEPActions = AccountIndexActionResponse &
    AccountReadActionResponse &
    ProfileIndexActionResponse &
    ProfileReadActionResponse;

