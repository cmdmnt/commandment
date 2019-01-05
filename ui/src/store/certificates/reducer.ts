import {combineReducers} from "redux";
import * as actions from "./actions";
import {
    DeleteCertificateActionResponse,
    IndexActionResponse,
} from "./actions";
import {FetchPushCertificatesActionResponse} from "./push_actions";

// Sub reducers
import {JSONAPIDataObject, JSONAPIDetailResponse} from "../json-api";
import {installed_certificates_reducer, InstalledCertificatesState} from "../device/installed_certificates_reducer";
import {ca, CAState} from "./ca_reducer";
import {push, PushState} from "./push_reducer";
import {ssl, SSLState} from "./ssl_reducer";
import {Certificate} from "./types";

export interface CertificatesState {
    items: Array<JSONAPIDataObject<Certificate>>;
    loading: boolean;
    error: boolean;
    errorDetail?: any
    lastReceived?: Date;
    currentPage: number;
    pageSize: number;
    recordCount?: number;
    byType?: { [propName: string]: JSONAPIDetailResponse<Certificate, undefined> };
    push?: PushState;
    ssl?: SSLState;
    ca?: CAState;
}

const initialState: CertificatesState = {
    items: [],
    loading: false,
    error: false,
    errorDetail: null,
    lastReceived: null,
    currentPage: 1,
    pageSize: 50,
    byType: {},
};

type CertificatesAction = IndexActionResponse | DeleteCertificateActionResponse;

export function certificates(state: CertificatesState = initialState, action: CertificatesAction): CertificatesState {
    switch (action.type) {
        case actions.INDEX_REQUEST:
            return {
                ...state,
                loading: true,
            };

        case actions.INDEX_FAILURE:
            return {
                ...state,
                error: true,
                errorDetail: action.payload,
            };

        case actions.INDEX_SUCCESS:
            return {
                ...state,
                items: action.payload.data,
                lastReceived: new Date,
                loading: false,
                recordCount: action.payload.meta.count,
            };

        case actions.DELETE_REQUEST:
            return {
                ...state,
                loading: true,
            };

        case actions.DELETE_FAILURE:
            return {
                ...state,
                loading: false,
                error: true,
                errorDetail: action.payload,
            };

        case actions.DELETE_SUCCESS:
            return state;

        default:
            return {
                ...state,
                push: push(state.push, action),
                ssl: ssl(state.ssl, action),
                ca: ca(state.ca, action),
            }
    }
}
