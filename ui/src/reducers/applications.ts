import {isJSONAPIErrorResponsePayload, JSONAPIDataObject} from "../json-api";
import {Application} from "../models";
import * as actions from "../actions/applications";
import {IResults, ResultsDefaultState} from "./interfaces";

export interface ApplicationsState extends IResults<Array<JSONAPIDataObject<Application>>> {
    allIds: string[];
}

const initialState: ApplicationsState = {
    ...ResultsDefaultState,
    allIds: [],
};

type ApplicationsAction = actions.IndexActionResponse | actions.PostActionResponse | actions.PatchActionResponse;

export function applications(state: ApplicationsState = initialState, action: ApplicationsAction): ApplicationsState {
    switch (action.type) {
        case actions.INDEX_REQUEST:
            return {
                ...state,
                loading: true,
            };
        case actions.INDEX_FAILURE:
            return {
                ...state,
                error: action.payload,
            };
        case actions.INDEX_SUCCESS:
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