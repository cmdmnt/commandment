import {createStore, applyMiddleware, compose} from 'redux';
import thunk from 'redux-thunk';
import {apiMiddleware} from 'redux-api-middleware';
import rootReducer from '../reducers';
import {Store} from "react-redux";
import {Middleware} from "redux";
import {RootState} from "../reducers/index";

export const configureStore = (initialState: RootState, ...middlewares: Array<Middleware> ): Store<any> => {

    const enhancer = compose(
        applyMiddleware(
            thunk,
            apiMiddleware,
            ...middlewares
        )
    )

    const store = createStore(
        rootReducer,
        initialState,
        enhancer
    )

    return store;
}

export default configureStore;