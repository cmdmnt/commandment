import {OtherAction} from "../constants";
import {isJSONAPIErrorResponsePayload, JSONAPIDataObject} from "../json-api";
import {
    InstalledProfilesActionResponse,
    PROFILES_SUCCESS,
} from "./profiles";
import {InstalledProfile} from "./types";

export interface InstalledProfilesState {
    items?: Array<JSONAPIDataObject<InstalledProfile>>;
    loading: boolean;
    pageSize: number;
    pages: number;
    recordCount: number;
}

const initialState: InstalledProfilesState = {
    items: [],
    loading: false,
    pageSize: 20,
    pages: 0,
    recordCount: 0,
};

type InstalledProfilesAction = InstalledProfilesActionResponse | OtherAction;

export function installed_profiles_reducer(state: InstalledProfilesState = initialState, action: InstalledProfilesAction): InstalledProfilesState {
    switch (action.type) {
        case PROFILES_SUCCESS:
            if (isJSONAPIErrorResponsePayload(action.payload)) {
                return state;
            } else {
                return {
                    ...state,
                    items: action.payload.data,
                    recordCount: action.payload.meta.count,
                };
            }
        default:
            return state;
    }
}
