import {routerReducer, RouterState} from "react-router-redux";
import {combineReducers} from "redux";
import { FormStateMap, reducer as formReducer } from "redux-form";

import {applications, ApplicationsState} from "../store/applications/applications";
import {configuration, ConfigurationState} from "../store/configuration/reducer";
import {dep, IDEPState} from "../store/dep/reducer";
import {device, DeviceState} from "../store/device/reducer";
import {devices, DevicesState} from "../store/devices/devices";
import {profiles, ProfilesState} from "../store/profiles/reducer";
import {tags, TagsState} from "../store/tags/reducer";
import {assistant, AssistantState} from "./assistant";
import {certificates, CertificatesState} from "./certificates";
import {commands, CommandsState} from "./commands";
import {device_groups, DeviceGroupsState} from "./device_groups";
import {organization, OrganizationState} from "./organization";
import {profile, ProfileState} from "./profile";

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
    applications,
    assistant,
    certificates,
    commands,
    configuration,
    dep,
    device,
    device_groups,
    devices,
    form: formReducer,
    organization,
    profile,
    profiles,
    router: routerReducer,
    tags,
});

export default rootReducer;
