import {combineReducers} from 'redux';
import {routerReducer, RouterState} from 'react-router-redux';
import { reducer as formReducer, FormStateMap } from 'redux-form';

import {certificates, CertificatesState} from './certificates';
import {assistant, AssistantState} from './assistant';

export interface RootState {
    router?: RouterState;
    form?: FormStateMap;
    certificates?: CertificatesState;
    assistant?: AssistantState;
}


export const rootReducer = combineReducers({
    router: routerReducer,
    form: formReducer,
    assistant,
    certificates
});

export default rootReducer;
