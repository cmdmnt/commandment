import {combineReducers} from 'redux';
import {scep, SCEPState} from "./configuration/scep";
import {vpp, VPPState} from "./configuration/vpp";
import {apns, APNSState} from "./settings/apns";

export interface ConfigurationState {
    scep?: SCEPState;
    vpp?: VPPState;
    apns?: APNSState;
}

const initialState: ConfigurationState = {
};

export function configuration(state: ConfigurationState = initialState, action: any): ConfigurationState {
    return combineReducers({
        scep,
        vpp,
        apns
    })(state, action);
}