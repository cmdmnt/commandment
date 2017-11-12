import * as React from 'react';
import { connect, Dispatch } from 'react-redux';

import {Navigation} from './Navigation';
import {Login} from '../components/Login';
// import {Sidebar} from './Sidebar';


export const UnconnectedApp: React.StatelessComponent = ({ children }) => (
    <div>
        <Navigation />
        <Login />
        {children}
    </div>
);

export const App = connect()(UnconnectedApp);