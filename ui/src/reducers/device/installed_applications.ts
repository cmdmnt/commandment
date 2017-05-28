import {
    APPLICATIONS_SUCCESS,
    InstalledApplicationsActionResponse
} from "../../actions/device/applications";
import {isJSONAPIErrorResponsePayload} from "../../constants";
import {InstalledApplication, JSONAPIObject} from "../../typings/definitions";

export interface InstalledApplicationsState {
    items?: Array<JSONAPIObject<InstalledApplication>>;
    recordCount: number;
}

const initialState: InstalledApplicationsState = {
    items: [],
    recordCount: 0
};

type InstalledCertificatesAction = InstalledApplicationsActionResponse;

export function installed_applications(state: InstalledApplicationsState = initialState, action: InstalledCertificatesAction): InstalledApplicationsState {
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
