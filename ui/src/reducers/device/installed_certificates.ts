import {
    READ_SUCCESS,
    ReadActionResponse
} from "../../actions/devices";
import {isJSONAPIErrorResponsePayload} from "../../constants";

interface CertificatesByDeviceId {
    [deviceId: number]: InstalledCertificate;
}

export interface InstalledCertificatesState {
    items: Array<JSONAPIObject<InstalledCertificate>>;
}

const initialState: InstalledCertificatesState = {
    items: []
};


type InstalledCertificatesAction = ReadActionResponse;

export function installed_certificates(state: InstalledCertificatesState, action: InstalledCertificatesAction): InstalledCertificatesState {
    switch (action.type) {
        case READ_SUCCESS:
            if (isJSONAPIErrorResponsePayload(action.payload)) {
                return {
                    ...state
                }
            } else {
                if (!action.payload.data.relationships) { return state; }
                if (!action.payload.data.relationships.hasOwnProperty('installed_certificates')) {
                    return state;
                }

                const items = action.payload.included.filter((item: JSONAPIObject<any>) => {
                    return item.type == 'installed_certificates';
                });

                return {
                    ...state,
                    items
                };
            }

        default:
            return state;
    }
}