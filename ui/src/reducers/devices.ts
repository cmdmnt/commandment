import {
    DevicesActionTypes,
    IndexActionResponse
} from "../actions/devices";
import {JSONAPIObject, isJSONAPIErrorResponsePayload} from "../json-api";
import {Device} from "../models";

export interface DeviceIdMap {
    [deviceId: string]: JSONAPIObject<Device>;
}

export interface DevicesState {
    items: Array<JSONAPIObject<Device>>;
    byId: DeviceIdMap;
    allIds: Array<string>;
    loading: boolean;
    error: boolean;
    errorDetail?: any
    lastReceived?: Date;
    currentPage: number;
    pageSize: number;
    recordCount?: number;
}

const initialState: DevicesState = {
    items: [],
    byId: {},
    allIds: [],
    loading: false,
    error: false,
    errorDetail: null,
    lastReceived: null,
    currentPage: 1,
    pageSize: 50
};

type DevicesAction = IndexActionResponse;

export function devices(state: DevicesState = initialState, action: DevicesAction): DevicesState {
    switch (action.type) {
        case DevicesActionTypes.INDEX_REQUEST:
            return {
                ...state,
                loading: true
            };

        case DevicesActionTypes.INDEX_FAILURE:
            return {
                ...state,
                error: true,
                errorDetail: action.payload
            };

        case DevicesActionTypes.INDEX_SUCCESS:
            if (isJSONAPIErrorResponsePayload(action.payload)) {
                return {
                    ...state,
                    loading: false,
                    error: true,
                    errorDetail: action.payload
                }
            } else {
                let allIds: string[] = [];
                const byId: DeviceIdMap = action.payload.data.reduce((memo: DeviceIdMap, device: JSONAPIObject<Device>) => {
                    memo[device.id] = device;
                    allIds.push(''+device.id);
                    return memo;
                }, {});

                return {
                    ...state,
                    byId,
                    allIds,
                    items: action.payload.data,
                    lastReceived: new Date,
                    loading: false,
                    recordCount: action.payload.meta.count
                };
            }

        // case actions.DELETE_REQUEST:
        //     return {
        //         ...state,
        //         loading: true
        //     };
        //
        // case actions.DELETE_FAILURE:
        //     return {
        //         ...state,
        //         loading: false,
        //         error: true,
        //         errorDetail: action.payload
        //     };
        //
        // case actions.DELETE_SUCCESS:
        //     return state;


        default:
            return state;
    }
}