/// <reference path="../../typings/redux-api-middleware.d.ts" />
import { RSAA, RSAAction } from "redux-api-middleware";
import {JSONAPI_HEADERS, JSONAPIDataObject, JSONAPIListResponse} from "../json-api";
import {Command} from "../device/types";

export type INDEX_REQUEST = "commands/INDEX_REQUEST";
export const INDEX_REQUEST: INDEX_REQUEST = "commands/INDEX_REQUEST";
export type INDEX_SUCCESS = "commands/INDEX_SUCCESS";
export const INDEX_SUCCESS: INDEX_SUCCESS = "commands/INDEX_SUCCESS";
export type INDEX_FAILURE = "commands/INDEX_FAILURE";
export const INDEX_FAILURE: INDEX_FAILURE = "commands/INDEX_FAILURE";

export type POST_REQUEST = "commands/POST_REQUEST";
export const POST_REQUEST: POST_REQUEST = "commands/POST_REQUEST";
export type POST_SUCCESS = "commands/POST_SUCCESS";
export const POST_SUCCESS: POST_SUCCESS = "commands/POST_SUCCESS";
export type POST_FAILURE = "commands/POST_FAILURE";
export const POST_FAILURE: POST_FAILURE = "commands/POST_FAILURE";

type PostActionRequest = (values: Command) => RSAAction<POST_REQUEST, POST_SUCCESS, POST_FAILURE>;

export interface PostActionResponse {
    type: POST_REQUEST | POST_FAILURE | POST_SUCCESS;
    payload?: JSONAPIListResponse<JSONAPIDataObject<Command>>;
}

export const post: PostActionRequest = (values: Command, device_id?: number) => {

    let endpoint = "/api/v1/commands";

    if (device_id) {
        endpoint = `/api/v1/devices/${device_id}/commands`;
    }

    return {
        [RSAA]: {
            body: JSON.stringify({
                data: {
                    attributes: values,
                    type: "commands",
                },
            }),
            endpoint,
            headers: JSONAPI_HEADERS,
            method: "POST",
            types: [
                POST_REQUEST,
                POST_SUCCESS,
                POST_FAILURE,
            ],
        },
    }
};
