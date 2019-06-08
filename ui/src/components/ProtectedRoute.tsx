import * as React from "react";
import {connect} from "react-redux";
import {FunctionComponent, Component} from "react";
import {Redirect, Route} from "react-router";
import {RootState} from "../reducers";

export interface IProtectedRoute {
    component: Component;
    access_token: string;
}

const UnconnectedProtectedRoute: FunctionComponent =
    ({component: Component, access_token, ...rest}: Partial<IProtectedRoute>) => (

    <Route
        {...rest}
        render={props => access_token ? (
            <Component {...props} />
        ) : (
            <Redirect to={{
                pathname: "/login",
                state: {from: props.location}
            }}/>
        )}
    />
);

export const ProtectedRoute = connect((state: RootState) => {
    return {
        access_token: state.auth.access_token,
        expires_in: state.auth.expires_in,
    }
}, null)(UnconnectedProtectedRoute);
