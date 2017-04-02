import {combineReducers} from 'redux';
import {routerReducer, RouterState} from 'react-router-redux';
import { reducer as formReducer, FormStateMap } from 'redux-form';

import {certificates, CertificatesState} from './certificates';
import {assistant, AssistantState} from './assistant';
import {config, ConfigState} from './config';
import {organization, OrganizationState} from './organization';

export interface RootState {
    router?: RouterState;
    form?: FormStateMap;
    certificates?: CertificatesState;
    assistant?: AssistantState;
    config?: ConfigState;
    organization?: OrganizationState;
}


export const rootReducer = combineReducers<RootState>({
    router: routerReducer,
    form: formReducer,
    assistant,
    certificates,
    config,
    organization
});

export default rootReducer;
