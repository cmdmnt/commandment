import * as actions from '../../actions/certificates/push';
import {JSONAPIListResponse, JSONAPIDataObject} from "../../json-api";
import {Certificate} from "../../models";

export interface PushState {
    items?: JSONAPIListResponse<JSONAPIDataObject<Certificate>>;
    loading: boolean;
    error: boolean;
    errorDetail?: any
    lastReceived?: Date;
}

const initialState: PushState = {
    loading: false,
    error: false,
    errorDetail: null,
    lastReceived: null
};

export type PushAction = actions.FetchPushCertificatesActionResponse;

export function push(state: PushState = initialState, action: PushAction): PushState {
    switch (action.type) {
        case actions.PUSHCERT_REQUEST:
            return {
                ...state,
                loading: true
            };
        case actions.PUSHCERT_FAILURE:
            return {
                ...state,
                loading: false,
                error: true,
                errorDetail: action.payload
            };
        case actions.PUSHCERT_SUCCESS:
            return {
                ...state,
                items: action.payload,
                lastReceived: new Date(),
                error: false,
                errorDetail: null
            };
        default:
            return state;
    }
}