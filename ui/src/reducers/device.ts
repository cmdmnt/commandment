import * as actions from '../actions/devices';
import {
    ReadActionResponse
} from "../actions/devices";
import {installed_certificates, InstalledCertificatesState} from "./device/installed_certificates";
import {isJSONAPIErrorResponsePayload} from "../constants";
import {commands, DeviceCommandsState} from "./device/commands";


export interface DeviceState {
    device?: JSONAPIObject<Device>;
    loading: boolean;
    error: boolean;
    errorDetail?: any
    lastReceived?: Date;
    currentPage: number;
    pageSize: number;
    recordCount?: number;
    certificates?: InstalledCertificatesState;
    commands?: DeviceCommandsState;
}

const initialState: DeviceState = {
    device: null,
    loading: false,
    error: false,
    errorDetail: null,
    lastReceived: null,
    currentPage: 1,
    pageSize: 50
};

type DevicesAction = ReadActionResponse;

export function device(state: DeviceState = initialState, action: DevicesAction): DeviceState {
    switch (action.type) {
        case actions.READ_REQUEST:
            return {
                ...state,
                loading: true
            };

        case actions.READ_FAILURE:
            return {
                ...state,
                error: true,
                errorDetail: action.payload
            };

        case actions.READ_SUCCESS:
            if (isJSONAPIErrorResponsePayload(action.payload)) {
                return {
                    ...state,
                    error: true,
                    errorDetail: action.payload
                }
            } else {
                return {
                    ...state,
                    device: action.payload.data,
                    lastReceived: new Date,
                    loading: false,
                    certificates: installed_certificates(state.certificates, action),
                    commands: commands(state.commands, action)
                };
            }
            
        default:
            return state;
    }
}