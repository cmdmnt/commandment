import {HTTPVerb, RSAA, RSAAction} from "redux-api-middleware";
import {
    encodeJSONAPIChildIndexParameters, encodeJSONAPIIndexParameters, JSONAPIDataObject, JSONAPIDetailResponse,
    JSONAPIListResponse,
    RSAAIndexActionRequest,
    RSAAIndexActionResponse, RSAAReadActionRequest, RSAAReadActionResponse,
} from "../json-api";
import {DeviceGroup} from "./types";
import {FlaskFilter, FlaskFilters, JSON_HEADERS, JSONAPI_HEADERS} from "../constants"
import {Device} from "../device/types";

export type INDEX_REQUEST = "device_groups/INDEX_REQUEST";
export const INDEX_REQUEST: INDEX_REQUEST = "device_groups/INDEX_REQUEST";
export type INDEX_SUCCESS = "device_groups/INDEX_SUCCESS";
export const INDEX_SUCCESS: INDEX_SUCCESS = "device_groups/INDEX_SUCCESS";
export type INDEX_FAILURE = "device_groups/INDEX_FAILURE";
export const INDEX_FAILURE: INDEX_FAILURE = "device_groups/INDEX_FAILURE";

export type IndexActionRequest = RSAAIndexActionRequest<INDEX_REQUEST, INDEX_SUCCESS, INDEX_FAILURE>;
export type IndexActionResponse = RSAAIndexActionResponse<INDEX_REQUEST, INDEX_SUCCESS, INDEX_FAILURE, DeviceGroup>;

export const index = encodeJSONAPIIndexParameters((queryParameters: String[]) => {
    return ({
        [RSAA]: {
            endpoint: "/api/v1/device_groups?" + queryParameters.join("&"),
            headers: JSONAPI_HEADERS,
            method: ("GET" as HTTPVerb),
            types: [
                INDEX_REQUEST,
                INDEX_SUCCESS,
                INDEX_FAILURE,
            ],
        },
    } as RSAAction<INDEX_REQUEST, INDEX_SUCCESS, INDEX_FAILURE>);
});

export type READ_REQUEST = "device_groups/READ_REQUEST";
export const READ_REQUEST: READ_REQUEST = "device_groups/READ_REQUEST";
export type READ_SUCCESS = "device_groups/READ_SUCCESS";
export const READ_SUCCESS: READ_SUCCESS = "device_groups/READ_SUCCESS";
export type READ_FAILURE = "device_groups/READ_FAILURE";
export const READ_FAILURE: READ_FAILURE = "device_groups/READ_FAILURE";

export type ReadActionRequest = RSAAReadActionRequest<READ_REQUEST, READ_SUCCESS, READ_FAILURE>;
export type ReadActionResponse = RSAAReadActionResponse<READ_REQUEST, READ_SUCCESS, READ_FAILURE, JSONAPIDetailResponse<DeviceGroup, undefined>>;

export const read: ReadActionRequest = (id: string, include?: string[]) => {

    let inclusions = "";
    if (include && include.length) {
        inclusions = "include=" + include.join(",")
    }

    return ({
        [RSAA]: {
            endpoint: `/api/v1/device_groups/${id}?${inclusions}`,
            method: "GET",
            types: [
                READ_REQUEST,
                READ_SUCCESS,
                READ_FAILURE,
            ],
            headers: JSONAPI_HEADERS,
        },
    } as RSAAction<READ_REQUEST, READ_SUCCESS, READ_FAILURE>);
};

export type POST_REQUEST = "device_groups/POST_REQUEST";
export const POST_REQUEST: POST_REQUEST = "device_groups/POST_REQUEST";
export type POST_SUCCESS = "device_groups/POST_SUCCESS";
export const POST_SUCCESS: POST_SUCCESS = "device_groups/POST_SUCCESS";
export type POST_FAILURE = "device_groups/POST_FAILURE";
export const POST_FAILURE: POST_FAILURE = "device_groups/POST_FAILURE";

type PostActionRequest = (values: DeviceGroup) => RSAAction<POST_REQUEST, POST_SUCCESS, POST_FAILURE>;

export interface PostActionResponse {
    type: POST_REQUEST | POST_FAILURE | POST_SUCCESS;
    payload?: JSONAPIListResponse<JSONAPIDataObject<DeviceGroup>>;
}

export const post: PostActionRequest = (values: DeviceGroup) => {

    return {
        [RSAA]: {
            body: JSON.stringify({
                data: {
                    attributes: values,
                    type: "reducer",
                },
            }),
            endpoint: `/api/v1/device_groups`,
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
