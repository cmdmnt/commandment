import {CommandsActionResponse, DevicesActionTypes} from "./actions";
import {JSONAPIDataObject, isJSONAPIErrorResponsePayload} from "../json-api";
import {Command} from "./types";
import {OtherAction} from "../constants";

export interface DeviceCommandsState {
    items?: Array<JSONAPIDataObject<Command>>;
    loading: boolean;
    pageSize: number;
    pages: number;
    recordCount: number;
}

const initialState: DeviceCommandsState = {
    items: [],
    loading: false,
    pageSize: 20,
    pages: 0,
    recordCount: 0,
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
                    pages: Math.floor(action.payload.meta.count / state.pageSize),
                    recordCount: action.payload.meta.count,
                };
            }
        default:
            return state;
    }
}
