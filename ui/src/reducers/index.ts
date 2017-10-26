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
import {device_groups, DeviceGroupsState} from "./device_groups";
import {tags, TagsState} from "./tags";
import {profile, ProfileState} from "./profile";
import {applications, ApplicationsState} from "./applications";

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
    device_groups?: DeviceGroupsState;
    tags?: TagsState;
    profile?: ProfileState;
    applications?: ApplicationsState;
}


export const rootReducer = combineReducers<RootState>({
    router: routerReducer,
    form: formReducer,
    applications,
    assistant,
    certificates,
    configuration,
    organization,
    devices,
    device,
    commands,
    profiles,
    device_groups,
    tags,
    profile
});

export default rootReducer;
