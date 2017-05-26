import {
    CERTIFICATES_SUCCESS,
    CertificatesActionResponse
} from "../../actions/devices";
import {isJSONAPIErrorResponsePayload} from "../../constants";
import {PageProperties} from "griddle-react";

export interface InstalledCertificatesState {
    items?: Array<InstalledCertificate>;
    pageProperties?: PageProperties;
}

const initialState: InstalledCertificatesState = {
    items: [],
    pageProperties: {
        currentPage: 1,
        pageSize: 20
    }
};


type InstalledCertificatesAction = CertificatesActionResponse;

export function installed_certificates(state: InstalledCertificatesState = initialState, action: InstalledCertificatesAction): InstalledCertificatesState {
    switch (action.type) {
        case CERTIFICATES_SUCCESS:
            if (isJSONAPIErrorResponsePayload(action.payload)) {
                return state;
            } else {
                const pageProperties = {
                    ...state.pageProperties,
                    recordCount: action.payload.meta.count
                };

                return {
                    ...state,
                    items: action.payload.data,
                    pageProperties
                };
            }
        default:
            return state;
    }
}