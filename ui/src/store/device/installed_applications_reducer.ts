import {
    APPLICATIONS_SUCCESS,
    InstalledApplicationsActionResponse
} from "./applications";
import {JSONAPIDataObject, isJSONAPIErrorResponsePayload} from "../../json-api";
import {InstalledApplication} from "./types";
import {OtherAction} from "../constants";

export interface InstalledApplicationsState {
    items?: Array<JSONAPIDataObject<InstalledApplication>>;
    recordCount: number;
}

const initialState: InstalledApplicationsState = {
    items: [],
    recordCount: 0
};

type InstalledCertificatesAction = InstalledApplicationsActionResponse | OtherAction;

export function installed_applications_reducer(state: InstalledApplicationsState = initialState, action: InstalledCertificatesAction): InstalledApplicationsState {
    switch (action.type) {
        case APPLICATIONS_SUCCESS:
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
