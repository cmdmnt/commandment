import {InstalledApplicationsActionResponse} from "./applications";
import {CertificatesActionResponse} from "./certificates";
import * as actions from "./actions";
import {
    CommandsActionResponse, PatchRelationshipActionResponse, PostRelatedActionResponse,
    ReadActionResponse,
} from "./actions";
import {DevicesActionTypes} from "./actions";
import {isArray} from "../../guards";
import {isJSONAPIErrorResponsePayload, JSONAPIDataObject} from "../../json-api";
import {Tag} from "../tags/types";
import {available_os_updates_reducer, AvailableOSUpdatesState} from "./available_os_updates_reducer";
import {commands_reducer, DeviceCommandsState} from "./commands_reducer";
import {installed_applications_reducer, InstalledApplicationsState} from "./installed_applications_reducer";
import {installed_certificates_reducer, InstalledCertificatesState} from "./installed_certificates_reducer";
import {installed_profiles_reducer, InstalledProfilesState} from "./installed_profiles_reducer";
import {Device} from "./types";

export interface DeviceState {
    device?: JSONAPIDataObject<Device>;
    loading: boolean;
    error: boolean;
    errorDetail?: any
    lastReceived?: Date;
    currentPage: number;
    pageSize: number;
    recordCount?: number;
    commands?: DeviceCommandsState;
    installed_certificates?: InstalledCertificatesState;
    installed_applications?: InstalledApplicationsState;
    installed_profiles?: InstalledProfilesState;
    available_os_updates?: AvailableOSUpdatesState;
    tags?: Array<JSONAPIDataObject<Tag>>;
    tagsLoading: boolean;
}

const initialState: DeviceState = {
    currentPage: 1,
    device: null,
    error: false,
    errorDetail: null,
    lastReceived: null,
    loading: false,
    pageSize: 50,
    tagsLoading: false,
};

type DevicesAction = ReadActionResponse | InstalledApplicationsActionResponse | CommandsActionResponse |
    CertificatesActionResponse | PatchRelationshipActionResponse | PostRelatedActionResponse;

export function device(state: DeviceState = initialState, action: DevicesAction): DeviceState {
    switch (action.type) {
        case DevicesActionTypes.READ_REQUEST:
            return {
                ...state,
                loading: true,
            };

        case DevicesActionTypes.READ_FAILURE:
            return {
                ...state,
                error: true,
                errorDetail: action.payload,
            };

        case DevicesActionTypes.READ_SUCCESS:
            if (isJSONAPIErrorResponsePayload(action.payload)) {
                return {
                    ...state,
                    error: true,
                    errorDetail: action.payload,
                }
            } else {
                let tags: Array<JSONAPIDataObject<Tag>> = [];

                if (action.payload.included) {
                    tags = action.payload.included.filter((included: JSONAPIDataObject<any>) => (included.type === "tags"));
                }

                return {
                    ...state,
                    device: action.payload.data,
                    lastReceived: new Date,
                    loading: false,
                    tags,
                };
            }
        case actions.RPATCH_REQUEST:
            return {
                ...state,
                tagsLoading: true,
            };
        case actions.RPATCH_SUCCESS:
            if (isJSONAPIErrorResponsePayload(action.payload)) {
                return {
                    ...state,
                    error: true,
                    errorDetail: action.payload,
                }
            } else {
                const device: JSONAPIDataObject<Device> = {
                    ...state.device,
                    relationships: {
                        ...state.device.relationships,
                        // tags: action.payload.data.relationships.tags,
                    },
                };

                return {
                    ...state,
                    device,
                    tagsLoading: false,
                };
            }

        case actions.RPATCH_FAILURE:
            return {
                ...state,
                tagsLoading: false,
            };

        case actions.RCPOST_REQUEST:
            return {
                ...state,
                tagsLoading: true,
            };

        case actions.RCPOST_SUCCESS:
            const data: any[] = isArray(action.payload.data) ? action.payload.data : [action.payload.data];
            const mergedTags = data.concat(state.device.relationships.tags.data);

            return {
                ...state,
                device: {
                    ...state.device,
                    relationships: {
                        ...state.device.relationships,
                        tags: {
                            data: mergedTags,
                        },
                    },
                },
            };

        case actions.RCPOST_FAILURE:
            return {
                ...state,
                error: true,
                errorDetail: action.payload,
                tagsLoading: false,
            };

        default:
            return {
                ...state,
                available_os_updates: available_os_updates_reducer(state.available_os_updates, action),
                commands: commands_reducer(state.commands, action),
                installed_applications: installed_applications_reducer(state.installed_applications, action),
                installed_certificates: installed_certificates_reducer(state.installed_certificates, action),
                installed_profiles: installed_profiles_reducer(state.installed_profiles, action),
            };
    }
}
