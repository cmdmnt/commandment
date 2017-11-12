import * as React from 'react';
import { connect } from 'react-redux';
import { login, logout } from 'redux-implicit-oauth2';

const config = {
    url: "https://accounts.google.com/o/oauth2/v2/auth",
    client: "18556572230-jbj8kqk6rivl5thble54ed0ioc3f65au.apps.googleusercontent.com",
    redirect: "https://commandment.dev:5443/oauth/authorize",
    scope: "https://www.googleapis.com/auth/drive.metadata.readonly",
    width: 400, // Width (in pixels) of login popup window. Optional, default: 400
    height: 400, // Height (in pixels) of login popup window. Optional, default: 400
};

const LoginUnconnected = ({ isLoggedIn, login, logout }) => {
    if (isLoggedIn) {
        return <button type='button' onClick={logout}>Logout</button>
    } else {
        return <button type='button' onClick={login}>Login</button>
    }
};

const mapStateToProps = ({ auth }) => ({
    isLoggedIn: auth.isLoggedIn,
});

const mapDispatchToProps = {
    login: () => login(config),
    logout,
};

export const Login = connect(mapStateToProps, mapDispatchToProps)(LoginUnconnected);
