import {INDEX_SUCCESS, IndexActionResponse} from "../actions/device_groups";
import {isJSONAPIErrorResponsePayload} from "../constants";
import {JSONAPIObject} from "../json-api";
import {DeviceGroup} from "../models";

export interface DeviceGroupsState {
    items?: Array<JSONAPIObject<DeviceGroup>>;
    recordCount: number;
}

const initialState: DeviceGroupsState = {
    items: [],
    recordCount: 0
};

type DeviceGroupsAction = IndexActionResponse;

export function device_groups(state: DeviceGroupsState = initialState, action: DeviceGroupsAction): DeviceGroupsState {
    switch (action.type) {
        case INDEX_SUCCESS:
            if (isJSONAPIErrorResponsePayload(action.payload)) {
                return state;
            } else {
                return {
                    ...state,
                    items: action.payload.data,
                    recordCount: action.payload.meta.count
                };
            }
        default:
            return state;
    }
}
