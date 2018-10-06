import {encodeJSONAPIIndexParameters, RSAAIndexActionRequest, RSAAIndexActionResponse} from "../../json-api";
import {DEPAccount} from "../../models";
import {HTTPVerb, RSAA, RSAAction} from "redux-api-middleware";
import {JSONAPI_HEADERS} from "../constants";

export enum DEPActionTypes {
    INDEX_REQUEST = "dep/INDEX_REQUEST",
    INDEX_SUCCESS = "dep/INDEX_SUCCESS",
    INDEX_FAILURE = "dep/INDEX_FAILURE",
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

export type DEPActions = IndexActionResponse;
