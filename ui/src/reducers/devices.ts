import * as actions from '../actions/devices';
import {
    IndexActionResponse
} from "../actions/devices";


export interface DevicesState {
    items: Array<JSONAPIObject<Device>>;
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
        case actions.INDEX_REQUEST:
            return {
                ...state,
                loading: true
            };

        case actions.INDEX_FAILURE:
            return {
                ...state,
                error: true,
                errorDetail: action.payload
            };

        case actions.INDEX_SUCCESS:
            return {
                ...state,
                items: action.payload.data,
                lastReceived: new Date,
                loading: false,
                recordCount: action.payload.meta.count
            };

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