import {
    CERTIFICATES_SUCCESS,
    CertificatesActionResponse
} from "./certificates";
import {JSONAPIDataObject, isJSONAPIErrorResponsePayload} from "../../json-api";
import {InstalledCertificate} from "./types";
import {OtherAction} from "../constants";

export interface InstalledCertificatesState {
    items?: Array<JSONAPIDataObject<InstalledCertificate>>;
    recordCount: number;
}

const initialState: InstalledCertificatesState = {
    items: [],
    recordCount: 0
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
                    recordCount: action.payload.meta.count
                };
            }
        default:
            return state;
    }
}