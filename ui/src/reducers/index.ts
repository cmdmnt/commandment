import {combineReducers} from 'redux';
import {routerReducer, RouterState} from 'react-router-redux';
import { reducer as formReducer, FormStateMap } from 'redux-form';

import {certificates, CertificatesState} from './certificates';
import {assistant, AssistantState} from './assistant';
import {config, ConfigState} from './config';

export interface RootState {
    router?: RouterState;
    form?: FormStateMap;
    certificates?: CertificatesState;
    assistant?: AssistantState;
    config?: ConfigState;
}


export const rootReducer = combineReducers<RootState>({
    router: routerReducer,
    form: formReducer,
    assistant,
    certificates,
    config
});

export default rootReducer;
