import {combineReducers} from 'redux';
import {routerReducer, RouterState} from 'react-router-redux';
import { reducer as formReducer, FormStateMap } from 'redux-form';

import {certificates, CertificatesState} from './certificates';
import {assistant, AssistantState} from './assistant';
import {configuration, ConfigurationState} from './configuration';
import {organization, OrganizationState} from './organization';
import {devices, DevicesState} from "./devices";
import {device, DeviceState} from "./device";
import {commands, CommandsState} from './commands';
import {profiles, ProfilesState} from './profiles';

export interface RootState {
    router?: RouterState;
    form?: FormStateMap;
    certificates?: CertificatesState;
    assistant?: AssistantState;
    configuration?: ConfigurationState;
    organization?: OrganizationState;
    devices?: DevicesState;
    device?: DeviceState;
    commands?: CommandsState;
    profiles?: ProfilesState;
}


export const rootReducer = combineReducers<RootState>({
    router: routerReducer,
    form: formReducer,
    assistant,
    certificates,
    configuration,
    organization,
    devices,
    device,
    commands,
    profiles
});

export default rootReducer;
