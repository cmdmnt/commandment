import {Reducer} from "redux";
import {IResults, ResultsDefaultState} from "../../reducers/interfaces";
import {isJSONAPIErrorResponsePayload, JSONAPIDataObject} from "../json-api";
import {ManagedApplicationsActions, ManagedApplicationsActionTypes} from "./managed";
import {ManagedApplication} from "./types";

export interface IManagedApplicationsState extends IResults<Array<JSONAPIDataObject<ManagedApplication>>> {

}

const initialState: IManagedApplicationsState = {
    ...ResultsDefaultState,
};

export const managed_applications: Reducer<IManagedApplicationsState, ManagedApplicationsActions> =
    (state = initialState, action) => {
    switch (action.type) {
        case ManagedApplicationsActionTypes.INDEX_REQUEST:
            return {
                ...state,
                loading: true,
            };
        case ManagedApplicationsActionTypes.INDEX_SUCCESS:
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
                    loading: false,
                    recordCount: action.payload.meta.count,
                };
            }
        case ManagedApplicationsActionTypes.INDEX_FAILURE:
            return {
                ...state,
                error: true,
                errorDetail: action.payload,
                loading: false,
            };
        default:
            return state;
    }
};
