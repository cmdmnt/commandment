import {
    UPDATES_SUCCESS,
    AvailableOSUpdatesActionResponse
} from "./updates";
import {JSONAPIDataObject, isJSONAPIErrorResponsePayload} from "../../json-api";
import {InstalledProfile} from "./types";
import {OtherAction} from "../../actions/constants";


export interface AvailableOSUpdatesState {
    items?: Array<JSONAPIDataObject<InstalledProfile>>;
    recordCount: number;
}

const initialState: AvailableOSUpdatesState = {
    items: [],
    recordCount: 0
};

type AvailableOSUpdatesAction = AvailableOSUpdatesActionResponse | OtherAction;

export function available_os_updates_reducer(state: AvailableOSUpdatesState = initialState, action: AvailableOSUpdatesAction): AvailableOSUpdatesState {
    switch (action.type) {
        case UPDATES_SUCCESS:
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
