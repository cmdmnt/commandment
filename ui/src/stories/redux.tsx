import * as React from 'react';
import {Provider} from 'react-redux';
import {combineReducers, compose, createStore} from 'redux';
import { reducer as formReducer } from 'redux-form'
import {addDecorator, Story, StoryDecorator} from '@kadira/storybook';

const composeEnhancers = (window as any).__REDUX_DEVTOOLS_EXTENSION_COMPOSE__ || compose;

const store = createStore(combineReducers({ form: formReducer }), composeEnhancers());

const StoreDecorator: StoryDecorator = (story) => (
    <Provider store={store}>
        { story() }
    </Provider>
);

addDecorator(StoreDecorator);