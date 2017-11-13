/// <reference path="../typings/redux-api-middleware.d.ts" />
import {Store} from "react-redux";
import {applyMiddleware, compose, createStore} from "redux";
import {Middleware} from "redux";
import {apiMiddleware} from "redux-api-middleware";
import thunk from "redux-thunk";
import rootReducer from "../reducers";
import {IRootState} from "../reducers/index";
import {oidcMiddleware} from "../reducers/oidc";

const composeEnhancers = (window as any).__REDUX_DEVTOOLS_EXTENSION_COMPOSE__ || compose;

export const configureStore = (initialState: IRootState, ...middlewares: Middleware[] ): Store<any> => {

    const enhancer = composeEnhancers(
        applyMiddleware(
            thunk,
            oidcMiddleware,
            apiMiddleware,
            ...middlewares,
        ),
    );

    const store = createStore(
        rootReducer,
        initialState,
        enhancer,
    );

    if (module.hot) {
        module.hot.accept("../reducers", () => {
            const nextRootReducer = require("../reducers").default;
            store.replaceReducer(nextRootReducer);
        });
    }

    return store;
};

export default configureStore;
