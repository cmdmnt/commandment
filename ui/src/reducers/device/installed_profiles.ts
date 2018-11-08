import {
    PROFILES_SUCCESS,
    InstalledProfilesActionResponse
} from "../../actions/device/profiles";
import {JSONAPIDataObject, isJSONAPIErrorResponsePayload} from "../../json-api";
import {InstalledProfile} from "../../models";
import {OtherAction} from "../../actions/constants";


export interface InstalledProfilesState {
    items?: Array<JSONAPIDataObject<InstalledProfile>>;
    recordCount: number;
}

const initialState: InstalledProfilesState = {
    items: [],
    recordCount: 0
};

type InstalledProfilesAction = InstalledProfilesActionResponse | OtherAction;

export function installed_profiles(state: InstalledProfilesState = initialState, action: InstalledProfilesAction): InstalledProfilesState {
    switch (action.type) {
        case PROFILES_SUCCESS:
            if (isJSONAPIErrorResponsePayload(action.payload)) {
                return state;
            } else {
                return {
                    ...state,
                    items: action.payload.data,
                    recordCount: action.payload.meta.count
                };
            }
        default:
            return state;
    }
}
