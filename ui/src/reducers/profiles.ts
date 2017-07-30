import * as actions from '../actions/profiles';
import {IndexActionResponse, UploadActionResponse} from '../actions/profiles';
import {JSONAPIObject, isJSONAPIErrorResponsePayload} from "../json-api";
import {Profile} from "../models";
import {ApiError} from "redux-api-middleware";

export interface ProfilesState {
    items: Array<JSONAPIObject<Profile>>;
    loading: boolean;
    error: boolean;
    errorDetail?: ApiError | any;
    lastReceived?: Date;
    pageProperties: any;
    uploading: boolean;
    uploadError: boolean;
    uploadErrorDetail?: ApiError;
}

const initialState: ProfilesState = {
    items: [],
    loading: false,
    error: false,
    errorDetail: null,
    lastReceived: null,
    pageProperties: {
        currentPage: 1,
        pageSize: 10,
        recordCount: 0
    },
    uploading: false,
    uploadError: false,
    uploadErrorDetail: null
};

type ProfilesAction = IndexActionResponse | UploadActionResponse;

export function profiles(state: ProfilesState = initialState, action: ProfilesAction): ProfilesState {
    switch (action.type) {
        case actions.INDEX_REQUEST:
            return {
                ...state,
                loading: true
            };

        case actions.INDEX_FAILURE:
            return {
                ...state,
                error: true,
                errorDetail: action.payload
            };

        case actions.INDEX_SUCCESS:
            if (isJSONAPIErrorResponsePayload(action.payload)) {
                return {
                    ...state,
                    loading: false,
                    error: true,
                    errorDetail: action.payload
                }    
            } else {
                return {
                    ...state,
                    items: action.payload.data,
                    lastReceived: new Date,
                    loading: false,
                    recordCount: action.payload.meta.count
                };
            }
        case actions.UPLOAD_FAILURE:
            return {
                ...state,
                uploading: false,
                uploadError: true,
                uploadErrorDetail: action.payload
            };
        default:
            return state;
    }
}