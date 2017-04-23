import * as actions from '../actions/devices';
import {
    ReadActionResponse
} from "../actions/devices";
import {installed_certificates, InstalledCertificatesState} from "./device/installed_certificates";


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
}

const initialState: DeviceState = {
    device: null,
    loading: false,
    error: false,
    errorDetail: null,
    lastReceived: null,
    currentPage: 1,
    pageSize: 50,
    certificates: {}
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
            return {
                ...state,
                device: action.payload.data,
                lastReceived: new Date,
                loading: false,
                certificates: installed_certificates(state.certificates, action)
            };

        default:
            return state;
    }
}