import {routerReducer as router, RouterState} from "react-router-redux";
import {combineReducers} from "redux";
import {FormStateMap, reducer as form} from "redux-form";
import {reducer as oidc, UserState} from "redux-oidc";

import {applications, ApplicationsState} from "./applications";
import {assistant, AssistantState} from "./assistant";
import {certificates, CertificatesState} from "./certificates";
import {commands, CommandsState} from "./commands";
import {configuration, ConfigurationState} from "./configuration";
import {device, DeviceState} from "./device";
import {device_groups, DeviceGroupsState} from "./device_groups";
import {devices, DevicesState} from "./devices";
import {organization, OrganizationState} from "./organization";
import {profile, ProfileState} from "./profile";
import {profiles, ProfilesState} from "./profiles";
import {tags, TagsState} from "./tags";

export interface IRootState {
    router?: RouterState;
    form?: FormStateMap;
    certificates?: CertificatesState;
    auth?: { isLoggedIn: boolean; token: string; };
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
    oidc?: UserState;
}

export const rootReducer = combineReducers<IRootState>({
    applications,
    assistant,
    certificates,
    commands,
    configuration,
    device,
    device_groups,
    devices,
    form,
    oidc,
    organization,
    profile,
    profiles,
    router,
    tags,
});

export default rootReducer;
