import {COMMANDS_SUCCESS, CommandsActionResponse} from "../../actions/devices";
import {isJSONAPIErrorResponsePayload} from "../../constants";
import {PageProperties} from "griddle-react";

export interface DeviceCommandsState {
    items?: Array<Command>;
    pageProperties?: PageProperties;
}

const initialState: DeviceCommandsState = {
    items: [],
    pageProperties: {
        currentPage: 1,
        pageSize: 20
    }
};

type DeviceCommandsAction = CommandsActionResponse;

export function commands(state: DeviceCommandsState = initialState, action: DeviceCommandsAction): DeviceCommandsState {
    switch (action.type) {
        case COMMANDS_SUCCESS:
            if (isJSONAPIErrorResponsePayload(action.payload)) {
                return state;
            } else {
                const pageProperties = {
                    ...state.pageProperties,
                    recordCount: action.payload.meta.count
                };

                return {
                    ...state,
                    items: action.payload.data,
                    pageProperties
                };
            }
        default:
            return state;
    }
}
