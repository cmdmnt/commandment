import {combineReducers} from 'redux';
import {scep, SCEPState} from "./configuration/scep";
import {vpp, VPPState} from "./configuration/vpp";

export interface ConfigurationState {
    scep?: SCEPState;
    vpp?: VPPState
}

const initialState: ConfigurationState = {
};

export function configuration(state: ConfigurationState = initialState, action: any): ConfigurationState {
    return combineReducers({
        scep,
        vpp
    })(state, action);
}