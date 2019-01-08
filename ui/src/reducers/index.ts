import {connectRouter, RouterState} from "connected-react-router";
import {combineReducers} from "redux";

import {applications, IApplicationsState} from "../store/applications/list_reducer";
import {application, IApplicationState} from "../store/applications/reducer";
import {assistant, IAssistantState} from "../store/assistant/reducer";
import {certificates, CertificatesState} from "../store/certificates/reducer";
import {commands, CommandsState} from "../store/commands/reducer";
import {configuration, ConfigurationState} from "../store/configuration/reducer";
import {dep, IDEPState} from "../store/dep/reducer";
import {device, DeviceState} from "../store/device/reducer";
import {device_groups, DeviceGroupsState} from "../store/device_groups/reducer";
import {devices, IDevicesState} from "../store/devices/devices";
import {organization, OrganizationState} from "../store/organization/reducer";
import {IProfileState, profile} from "../store/profile/reducer";
import {profiles, ProfilesState} from "../store/profiles/reducer";
import {ITableState, table} from "../store/table/reducer";
import {ITagsState, tags} from "../store/tags/reducer";

export interface RootState {
    router?: RouterState;

    certificates?: CertificatesState;
    assistant?: IAssistantState;
    configuration?: ConfigurationState;
    organization?: OrganizationState;
    devices?: IDevicesState;
    device?: DeviceState;
    commands?: CommandsState;
    profiles?: ProfilesState;
    device_groups?: DeviceGroupsState;
    tags?: ITagsState;
    profile?: IProfileState;
    applications?: IApplicationsState;
    application?: IApplicationState;
    dep?: IDEPState;
    table?: ITableState;
}

export const rootReducer = (history: any) => combineReducers<RootState>({
    application,
    applications,
    assistant,
    certificates,
    commands,
    configuration,
    dep,
    device,
    device_groups,
    devices,
    organization,
    profile,
    profiles,
    router: connectRouter(history),
    table,
    tags,
});

export default rootReducer;
