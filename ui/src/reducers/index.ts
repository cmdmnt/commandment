import {combineReducers} from 'redux';
import {routerReducer} from 'react-router-redux';

import {certificates} from './certificates';

export interface RootState {
        
}


export const rootReducer = combineReducers({
    router: routerReducer,
    certificates
});

export default rootReducer;
