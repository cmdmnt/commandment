import {routerReducer, RouterState} from "react-router-redux";
import {combineReducers} from "redux";
import { FormStateMap, reducer as formReducer } from "redux-form";

import {applications, ApplicationsState} from "../store/applications/applications";
import {certificates, CertificatesState} from "../store/certificates/reducer";
import {configuration, ConfigurationState} from "../store/configuration/reducer";
import {dep, IDEPState} from "../store/dep/reducer";
import {device, DeviceState} from "../store/device/reducer";
import {device_groups, DeviceGroupsState} from "../store/device_groups/reducer";
import {devices, DevicesState} from "../store/devices/devices";
import {organization, OrganizationState} from "../store/organization/reducer";
import {profiles, ProfilesState} from "../store/profiles/reducer";
import {ITableState, table} from "../store/table/reducer";
import {tags, ITagsState} from "../store/tags/reducer";
import {assistant, AssistantState} from "./assistant";
import {commands, CommandsState} from "./commands";
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
    tags?: ITagsState;
    profile?: ProfileState;
    applications?: ApplicationsState;
    dep?: IDEPState;
    table?: ITableState;
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
    table,
    tags,
});

export default rootReducer;
