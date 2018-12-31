import {
    CERTIFICATES_SUCCESS,
    CertificatesActionResponse
} from "./certificates";
import {JSONAPIDataObject, isJSONAPIErrorResponsePayload} from "../../json-api";
import {InstalledCertificate} from "./types";
import {OtherAction} from "../constants";

export interface InstalledCertificatesState {
    items?: Array<JSONAPIDataObject<InstalledCertificate>>;
    pageSize: number;
    pages: number;
    recordCount: number;
}

const initialState: InstalledCertificatesState = {
    items: [],
    pageSize: 20,
    pages: 0,
    recordCount: 0,
};

type InstalledCertificatesAction = CertificatesActionResponse | OtherAction;

export function installed_certificates_reducer(state: InstalledCertificatesState = initialState, action: InstalledCertificatesAction): InstalledCertificatesState {
    switch (action.type) {
        case CERTIFICATES_SUCCESS:
            if (isJSONAPIErrorResponsePayload(action.payload)) {
                return state;
            } else {
                return {
                    ...state,
                    items: action.payload.data,
                    pages: Math.floor(action.payload.meta.count / state.pageSize),
                    recordCount: action.payload.meta.count,
                };
            }
        default:
            return state;
    }
}