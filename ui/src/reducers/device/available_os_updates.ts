import {
    UPDATES_SUCCESS,
    AvailableOSUpdatesActionResponse
} from "../../actions/device/updates";
import {JSONAPIObject, isJSONAPIErrorResponsePayload} from "../../json-api";
import {InstalledProfile} from "../../models";
import {OtherAction} from "../../actions/constants";


export interface AvailableOSUpdatesState {
    items?: Array<JSONAPIObject<InstalledProfile>>;
    recordCount: number;
}

const initialState: AvailableOSUpdatesState = {
    items: [],
    recordCount: 0
};

type AvailableOSUpdatesAction = AvailableOSUpdatesActionResponse | OtherAction;

export function available_os_updates(state: AvailableOSUpdatesState = initialState, action: AvailableOSUpdatesAction): AvailableOSUpdatesState {
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
