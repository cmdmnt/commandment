import * as actions from '../actions/devices';
import {
    CommandsActionResponse,
    ReadActionResponse
} from "../actions/devices";
import {CertificatesActionResponse} from '../actions/device/certificates';
import {commands, DeviceCommandsState} from "./device/commands";
import {installed_certificates, InstalledCertificatesState} from "./device/installed_certificates";
import {installed_applications, InstalledApplicationsState} from "./device/installed_applications";
import {InstalledApplicationsActionResponse} from "../actions/device/applications";
import {installed_profiles, InstalledProfilesState} from "./device/installed_profiles";
import {JSONAPIObject, isJSONAPIErrorResponsePayload} from "../json-api";
import {Device} from "../models";


export interface DeviceState {
    device?: JSONAPIObject<Device>;
    loading: boolean;
    error: boolean;
    errorDetail?: any
    lastReceived?: Date;
    currentPage: number;
    pageSize: number;
    recordCount?: number;
    commands?: DeviceCommandsState;
    installed_certificates?: InstalledCertificatesState;
    installed_applications?: InstalledApplicationsState;
    installed_profiles?: InstalledProfilesState;
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

type DevicesAction = ReadActionResponse | InstalledApplicationsActionResponse | CommandsActionResponse |
    CertificatesActionResponse;

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
                };
            }
            
        default:
            return {
                ...state,
                commands: commands(state.commands, action),
                installed_certificates: installed_certificates(state.installed_certificates, action),
                installed_applications: installed_applications(state.installed_applications, action),
                installed_profiles: installed_profiles(state.installed_profiles, action)
            };
    }
}