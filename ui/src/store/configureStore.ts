import {createStore, applyMiddleware, compose} from 'redux';
import thunk from 'redux-thunk';
import {apiMiddleware} from 'redux-api-middleware';
import rootReducer from '../reducers';
import {Store} from "react-redux";
import {Middleware} from "redux";
import {RootState} from "../reducers/index";

const composeEnhancers = (<any>window).__REDUX_DEVTOOLS_EXTENSION_COMPOSE__ || compose;

export const configureStore = (initialState: RootState, ...middlewares: Array<Middleware> ): Store<any> => {

    const enhancer = composeEnhancers(
        applyMiddleware(
            thunk,
            apiMiddleware,
            ...middlewares
        )
    );

    const store = createStore(
        rootReducer,
        initialState,
        enhancer
    );

    if (module.hot) {
        module.hot.accept('../reducers', () => {
            const nextRootReducer = require('../reducers').default;
            store.replaceReducer(nextRootReducer)
        });
    }

    return store;
};

export default configureStore;