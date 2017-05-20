

import {READ_SUCCESS, ReadActionResponse} from "../../actions/devices";
import {isJSONAPIErrorResponsePayload} from "../../constants";
export interface DeviceCommandsState {
    items?: Array<JSONAPIObject<Command>>;
}

const initialState: DeviceCommandsState = {
    items: []
};

type DeviceCommandsAction = ReadActionResponse;

export function commands(state: DeviceCommandsState = initialState, action: DeviceCommandsAction): DeviceCommandsState {
    switch (action.type) {
        case READ_SUCCESS:
            if (isJSONAPIErrorResponsePayload(action.payload)) {
                return state;
            } else {
                if (!action.payload.hasOwnProperty('included')) { return state; }

                const items = action.payload.included.filter((item: JSONAPIObject<any>) => {
                    return item.type == 'commands';
                });

                return {
                    ...state,
                    items
                };
            }
        default:
            return state;
    }
}
