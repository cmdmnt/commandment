import {combineReducers} from 'redux';
import {scep, SCEPState} from "./configuration/scep";

export interface ConfigurationState {
    scep?: SCEPState;
}

const initialState: ConfigurationState = {
    scep: {}
};

export function configuration(state: ConfigurationState = initialState, action: any): ConfigurationState {
    return combineReducers({
        scep
    });
}