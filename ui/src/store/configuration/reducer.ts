import {combineReducers} from "redux";

import {apns, APNSState} from "./apns_reducer";
import {scep, SCEPState} from "./scep_reducer";
import {vpp, VPPState} from "./vpp_reducer";

export interface ConfigurationState {
    scep: SCEPState;
    vpp: VPPState;
    apns: APNSState;
}

const initialState: ConfigurationState = {
    apns: null,
    scep: null,
    vpp: null,
};

export function configuration(state: ConfigurationState = initialState, action: any): ConfigurationState {
    return combineReducers({
        apns,
        scep,
        vpp,
    })(state, action);
}
