import * as actions from "./actions";
import {IndexActionResponse, UploadActionResponse} from "./actions";
import {JSONAPIDataObject, isJSONAPIErrorResponsePayload} from "../json-api";
import {Profile} from "./types";
import {ApiError} from "redux-api-middleware";
import {isApiError} from "../../guards";
import {IResults, ResultsDefaultState} from "../../reducers/interfaces";
import {ProfilesActionTypes} from "./actions";

export interface ProfilesState extends IResults<Array<JSONAPIDataObject<Profile>>> {
    pageProperties: any;
    uploading: boolean;
    uploadError: boolean;
    uploadErrorDetail?: ApiError;
}

const initialState: ProfilesState = {
    ...ResultsDefaultState,
    pageProperties: {
        currentPage: 1,
        pageSize: 10,
        recordCount: 0,
    },
    uploadError: false,
    uploadErrorDetail: null,
    uploading: false,
};

type ProfilesAction = IndexActionResponse | UploadActionResponse;

export function profiles(state: ProfilesState = initialState, action: ProfilesAction): ProfilesState {
    switch (action.type) {
        case ProfilesActionTypes.INDEX_REQUEST:
            return {
                ...state,
                loading: true,
            };

        case ProfilesActionTypes.INDEX_FAILURE:
            return {
                ...state,
                error: action.payload,
            };

        case ProfilesActionTypes.INDEX_SUCCESS:
            if (isJSONAPIErrorResponsePayload(action.payload)) {
                return {
                    ...state,
                    error: action.payload,
                    loading: false,
                };
            } else {
                return {
                    ...state,
                    items: action.payload.data,
                    lastReceived: new Date(),
                    loading: false,
                    recordCount: action.payload.meta.count,
                };
            }
        case actions.UPLOAD_FAILURE:
            if (isApiError(action.payload)) {
                return {
                    ...state,
                    uploadError: true,
                    uploadErrorDetail: action.payload,
                    uploading: false,
                };
            }
        default:
            return state;
    }
}
