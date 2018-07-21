import {combineReducers} from 'redux';
import {dep, DEPState} from "./configuration/dep";
import {scep, SCEPState} from "./configuration/scep";
import {vpp, VPPState} from "./configuration/vpp";

export interface ConfigurationState {
    scep?: SCEPState;
    vpp?: VPPState;
    dep?: DEPState;
}

const initialState: ConfigurationState = {
};

export function configuration(state: ConfigurationState = initialState, action: any): ConfigurationState {
    return combineReducers({
        scep,
        vpp,
        dep
    })(state, action);
}