import * as actions from '../../actions/certificates/ca';
import {JSONAPIListResponse, JSONAPIDataObject} from "../../json-api";
import {Certificate} from "../../models";

export interface CAState {
    items?: JSONAPIListResponse<JSONAPIDataObject<Certificate>>;
    loading: boolean;
    error: boolean;
    errorDetail?: any
    lastReceived?: Date;
}

const initialState: CAState = {
    loading: false,
    error: false,
    errorDetail: null,
    lastReceived: null
};

export type PushAction = actions.FetchCACertificatesActionResponse;

export function ca(state: CAState = initialState, action: PushAction): CAState {
    switch (action.type) {
        case actions.CACERT_REQUEST:
            return {
                ...state,
                loading: true
            };
        case actions.CACERT_FAILURE:
            return {
                ...state,
                loading: false,
                error: true,
                errorDetail: action.payload
            };
        case actions.CACERT_SUCCESS:
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