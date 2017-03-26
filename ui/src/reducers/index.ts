import {combineReducers} from 'redux';
import {routerReducer, RouterState} from 'react-router-redux';

import {certificates, CertificatesState} from './certificates';

export interface RootState {
    router?: RouterState;
    certificates?: CertificatesState;
}


export const rootReducer = combineReducers({
    router: routerReducer,
    certificates
});

export default rootReducer;
