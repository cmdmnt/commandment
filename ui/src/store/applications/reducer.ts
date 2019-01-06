import {IResults, ResultsDefaultState} from "../../reducers/interfaces";
import {isJSONAPIErrorResponsePayload, JSONAPIDataObject} from "../json-api";
import {ApplicationsActions, ApplicationsActionTypes} from "./actions";
import {Application} from "./types";

export interface IApplicationsState extends IResults<Array<JSONAPIDataObject<Application>>> {
    allIds: string[];
}

const initialState: IApplicationsState = {
    ...ResultsDefaultState,
    allIds: [],
};

export function applications(state: IApplicationsState = initialState,
                             action: ApplicationsActions): IApplicationsState {
    switch (action.type) {
        case ApplicationsActionTypes.INDEX_REQUEST:
            return {
                ...state,
                loading: true,
            };
        case ApplicationsActionTypes.INDEX_FAILURE:
            return {
                ...state,
                error: action.payload,
            };
        case ApplicationsActionTypes.INDEX_SUCCESS:
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
        default:
            return state;
    }
}
