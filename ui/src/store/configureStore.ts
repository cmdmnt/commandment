import {applyMiddleware, compose, createStore, Store} from "redux";
import {Middleware} from "redux";
import {apiMiddleware} from "redux-api-middleware";
import thunk from "redux-thunk";
import rootReducer from "../reducers";
import {RootState} from "../reducers/index";

const composeEnhancers = (window as any).__REDUX_DEVTOOLS_EXTENSION_COMPOSE__ || compose;

export const configureStore = (initialState: RootState, ...middlewares: Middleware[] ): Store<any> => {

    const enhancer = composeEnhancers(
        applyMiddleware(
            thunk,
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
            store.replaceReducer(nextRootReducer)
        });
    }

    return store;
};

export default configureStore;
