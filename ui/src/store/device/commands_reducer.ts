import {CommandsActionResponse, DevicesActionTypes} from "../../actions/devices";
import {JSONAPIDataObject, isJSONAPIErrorResponsePayload} from "../../json-api";
import {Command} from "../../models";
import {OtherAction} from "../../actions/constants";

export interface DeviceCommandsState {
    items?: Array<JSONAPIDataObject<Command>>;
    recordCount: number;
}

const initialState: DeviceCommandsState = {
    items: [],
    recordCount: 0
};

type DeviceCommandsAction = CommandsActionResponse | OtherAction;

export function commands_reducer(state: DeviceCommandsState = initialState, action: DeviceCommandsAction): DeviceCommandsState {
    switch (action.type) {
        case DevicesActionTypes.COMMANDS_SUCCESS:
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
