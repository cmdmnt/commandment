import * as React from "react";

import {connect} from "react-redux";
import {Redirect, RouteComponentProps, RouteProps} from "react-router";
import {Grid, Card, Checkbox, Form, Header, Input, Message} from "semantic-ui-react";
import * as actions from "../store/auth/actions";
import {
    Formik,
    FormikActions,
    FormikProps,
    Form as FormikForm,
    Field,
    FieldProps,
    Label,
    withFormik,
    FormikBag
} from "formik";
import { Button } from "formik-semantic-ui";
import {RootState} from "../reducers";
import {ApiError} from "redux-api-middleware";
import * as Yup from "yup";

interface IFormValues {
    email: string;
    password: string;
}

interface IReduxDispatchProps {
    logout: actions.TokenActionRequestCreator;
}

export interface ILogoutPageProps extends IReduxDispatchProps {
    apiError?: ApiError;
    access_token?: string;
    loading: boolean;
}

export interface IRouteProps {
    from?: string;
}

const UnconnectedLogoutPage: React.FC = (
    props: ILogoutPageProps & RouteComponentProps<IRouteProps>) => {

    return (
        <Grid textAlign="center" style={{height: '100vh'}} verticalAlign="middle">
            <Grid.Column style={{maxWidth: 450}}>
                <Card>
                    <Card.Content>
                        <Card.Header>Logging Out</Card.Header>
                        <Card.Description>
                            Hold on while we log you out...
                        </Card.Description>
                    </Card.Content>
                </Card>
            </Grid.Column>}
        </Grid>
    );
};

export const LogoutPage = connect(
    (state: RootState) => ({
        access_token: state.auth.access_token,
        apiError: state.auth.error,
        loading: state.auth.loading,
    }),
    {Logout: actions.logout})(UnconnectedLogoutPage);
