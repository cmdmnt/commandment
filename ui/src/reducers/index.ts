import {routerReducer, RouterState} from "react-router-redux";
import {combineReducers} from "redux";
import { FormStateMap, reducer as formReducer } from "redux-form";

import {dep, IDEPState} from "../store/dep/reducer";
import {device, DeviceState} from "../store/device/reducer";
import {devices, DevicesState} from "../store/devices/devices";
import {profiles, ProfilesState} from "../store/profiles/reducer";
import {applications, ApplicationsState} from "./applications";
import {assistant, AssistantState} from "./assistant";
import {certificates, CertificatesState} from "./certificates";
import {commands, CommandsState} from "./commands";
import {configuration, ConfigurationState} from "./configuration";
import {device_groups, DeviceGroupsState} from "./device_groups";
import {organization, OrganizationState} from "./organization";
import {profile, ProfileState} from "./profile";
import {tags, TagsState} from "../store/tags/reducer";

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
    dep?: IDEPState;
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
    profile,
    dep,
});

export default rootReducer;
