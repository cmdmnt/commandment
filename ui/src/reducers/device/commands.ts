import {COMMANDS_SUCCESS, CommandsActionResponse} from "../../actions/devices";
import {isJSONAPIErrorResponsePayload} from "../../constants";
import {Command, JSONAPIObject} from "../../typings/definitions";

export interface DeviceCommandsState {
    items?: Array<JSONAPIObject<Command>>;
    recordCount: number;
}

const initialState: DeviceCommandsState = {
    items: [],
    recordCount: 0
};

type DeviceCommandsAction = CommandsActionResponse;

export function commands(state: DeviceCommandsState = initialState, action: DeviceCommandsAction): DeviceCommandsState {
    switch (action.type) {
        case COMMANDS_SUCCESS:
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
