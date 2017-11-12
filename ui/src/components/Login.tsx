import * as React from 'react';
import { connect } from 'react-redux';
import { login, logout } from 'redux-implicit-oauth2';

const config = {

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
