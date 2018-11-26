import {isJSONAPIErrorResponsePayload, JSONAPIDataObject} from "../../json-api";
import {
    DevicesActionTypes,
    IndexActionResponse,
} from "../device/actions";
import {Device} from "../device/types";

export interface DeviceIdMap {
    [deviceId: string]: JSONAPIDataObject<Device>;
}

export interface DevicesState {
    items: Array<JSONAPIDataObject<Device>>;
    byId: DeviceIdMap;
    allIds: string[];
    loading: boolean;
    error: boolean;
    errorDetail?: any
    lastReceived?: Date;
    currentPage: number;
    pageSize: number;
    recordCount?: number;
}

const initialState: DevicesState = {
    allIds: [],
    byId: {},
    currentPage: 1,
    error: false,
    errorDetail: null,
    items: [],
    lastReceived: null,
    loading: false,
    pageSize: 50,
};

type DevicesAction = IndexActionResponse;

export function devices(state: DevicesState = initialState, action: DevicesAction): DevicesState {
    switch (action.type) {
        case DevicesActionTypes.INDEX_REQUEST:
            return {
                ...state,
                loading: true,
            };

        case DevicesActionTypes.INDEX_FAILURE:
            return {
                ...state,
                error: true,
                errorDetail: action.payload,
            };

        case DevicesActionTypes.INDEX_SUCCESS:
            if (isJSONAPIErrorResponsePayload(action.payload)) {
                return {
                    ...state,
                    error: true,
                    errorDetail: action.payload,
                    loading: false,
                }
            } else {
                const allIds: string[] = [];
                const byId: DeviceIdMap = action.payload.data.reduce((memo: DeviceIdMap, device: JSONAPIDataObject<Device>) => {
                    memo[device.id] = device;
                    allIds.push("" + device.id);
                    return memo;
                }, {});

                return {
                    ...state,
                    allIds,
                    byId,
                    items: action.payload.data,
                    lastReceived: new Date,
                    loading: false,
                    recordCount: action.payload.meta.count,
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
