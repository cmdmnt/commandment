import * as actions from '../actions/certificates';
import {
    FetchCertificateTypeActionResponse, FetchPushCertificateActionResponse,
    IndexActionResponse
} from "../actions/certificates";


export interface CertificatesState {
    items: Array<JSONAPIObject<Certificate>>;
    loading: boolean;
    error: boolean;
    errorDetail?: any
    lastReceived?: Date;
    currentPage: number;
    pageSize: number;
    recordCount?: number;
    byType?: { [propName: string]: JSONAPIDetailResponse<Certificate> };
}

const initialState: CertificatesState = {
    items: [],
    loading: false,
    error: false,
    errorDetail: null,
    lastReceived: null,
    currentPage: 1,
    pageSize: 50,
    byType: {}
};

type CertificatesAction = IndexActionResponse | FetchCertificateTypeActionResponse;

export function certificates(state: CertificatesState = initialState, action: CertificatesAction): CertificatesState {
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

        case actions.CERTTYPE_REQUEST:
            return {
                ...state,
                loading: true
            };

        case actions.CERTTYPE_FAILURE:
            return {
                ...state,
                loading: false,
                error: true,
                errorDetail: action.payload
            };

        case actions.CERTTYPE_SUCCESS:
            return {
                ...state,
                loading: false,
                error: false,
                errorDetail: null,
                byType: {
                    ...state.byType,
                    [action.payload.data.attributes.purpose]: action.payload
                }
            };

        default:
            return state
    }
}