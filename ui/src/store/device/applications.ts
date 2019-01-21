import {JSONAPI_HEADERS} from "../constants";
import {RSAA, HTTPVerb, RSAAction} from "redux-api-middleware";
import {
    RSAAChildIndexActionRequest, RSAAIndexActionResponse
} from "../json-api";
import {InstalledApplication} from "./types";
import {encodeJSONAPIChildIndexParameters} from "../../flask-rest-jsonapi";


export type APPLICATIONS_REQUEST = 'devices/APPLICATIONS_REQUEST';
export const APPLICATIONS_REQUEST: APPLICATIONS_REQUEST = 'devices/APPLICATIONS_REQUEST';
export type APPLICATIONS_SUCCESS = 'devices/APPLICATIONS_SUCCESS';
export const APPLICATIONS_SUCCESS: APPLICATIONS_SUCCESS = 'devices/APPLICATIONS_SUCCESS';
export type APPLICATIONS_FAILURE = 'devices/APPLICATIONS_FAILURE';
export const APPLICATIONS_FAILURE: APPLICATIONS_FAILURE = 'devices/APPLICATIONS_FAILURE';

export type InstalledApplicationsActionRequest = RSAAChildIndexActionRequest<APPLICATIONS_REQUEST, APPLICATIONS_SUCCESS, APPLICATIONS_FAILURE>;
export type InstalledApplicationsActionResponse = RSAAIndexActionResponse<APPLICATIONS_REQUEST, APPLICATIONS_SUCCESS, APPLICATIONS_FAILURE, InstalledApplication>;

/**
 *
 * @type {(id:number, size?:number, pageNumber?:number, sort?:String[], filters?:FlaskFilters)=>R}
 */
export const applications = encodeJSONAPIChildIndexParameters((device_id: string, queryParameters: Array<String>)  => {
    return (<RSAAction<APPLICATIONS_REQUEST, APPLICATIONS_SUCCESS, APPLICATIONS_FAILURE>>{
        [RSAA]: {
            endpoint: `/api/v1/devices/${device_id}/installed_applications?${queryParameters.join('&')}`,
            method: (<HTTPVerb>'GET'),
            types: [
                APPLICATIONS_REQUEST,
                APPLICATIONS_SUCCESS,
                APPLICATIONS_FAILURE
            ],
            headers: JSONAPI_HEADERS
        }
    });
});
