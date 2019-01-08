import {JSONAPIDetailResponse} from "../json-api";
import {ApplicationsActions, ApplicationsActionTypes} from "./actions";
import {Application} from "./types";

export interface IApplicationState {
    loading: boolean;
    data: JSONAPIDetailResponse<Application, void>;
    error: boolean;
    errorDetail: any;
}

const initialState: IApplicationState = {
    data: null,
    error: false,
    errorDetail: null,
    loading: false,
};

export function application(state: IApplicationState = initialState, action: ApplicationsActions) {
    switch (action.type) {
        case ApplicationsActionTypes.READ_REQUEST:
            return {
                ...state,
                data: null,
                error: false,
                errorDetail: null,
                loading: true,
            };
        case ApplicationsActionTypes.READ_SUCCESS:
            return {
                ...state,
                data: action.payload,
                loading: false,
            };
        case ApplicationsActionTypes.READ_FAILURE:
            return {
                ...state,
                data: null,
                error: true,
                errorDetail: action.payload,
                loading: false,
            };
        default:
            return state;
    }
}
