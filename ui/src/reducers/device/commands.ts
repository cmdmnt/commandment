import {COMMANDS_SUCCESS, CommandsActionResponse} from "../../actions/devices";
import {JSONAPIObject, isJSONAPIErrorResponsePayload} from "../../json-api";
import {Command} from "../../models";
import {OtherAction} from "../../actions/constants";

export interface DeviceCommandsState {
    items?: Array<JSONAPIObject<Command>>;
    recordCount: number;
}

const initialState: DeviceCommandsState = {
    items: [],
    recordCount: 0
};

type DeviceCommandsAction = CommandsActionResponse | OtherAction;

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
