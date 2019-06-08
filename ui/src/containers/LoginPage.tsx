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
    login: actions.TokenActionRequestCreator;
}

export interface ILoginPageProps extends IReduxDispatchProps {
    apiError?: ApiError;
    access_token?: string;
    loading: boolean;
}

export interface IRouteProps {
    from?: string;
}

const UnconnectedLoginPage: React.FC = (
    props: ILoginPageProps & RouteComponentProps<IRouteProps> & FormikProps<IFormValues>) => {
    const { touched, errors, isSubmitting, handleBlur, handleChange, values, handleSubmit, login, loading, apiError,
        access_token } = props;

    return (
        <Grid textAlign="center" style={{height: '100vh'}} verticalAlign="middle">
            {access_token ? <Redirect to={{
                pathname: "/",
            }}/> :
            <Grid.Column style={{maxWidth: 450}}>
                <Card>
                    <Card.Content>
                        <Card.Header>Sign in</Card.Header>
                        <Card.Description>
                            <Form size="large" onSubmit={handleSubmit}>
                                <Form.Field required>
                                    <Input
                                        name="email"
                                        fluid
                                        icon="user"
                                        iconPosition="left"
                                        placeholder="E-mail address"
                                        onChange={handleChange} onBlur={handleBlur}
                                        value={values.email}
                                    />
                                    {errors.email &&
                                    touched.email &&
                                    <Label pointing>{errors.email}</Label>}
                                </Form.Field>
                                <Form.Field required>
                                    <Input
                                        name="password"
                                        fluid
                                        icon="lock"
                                        iconPosition="left"
                                        placeholder="Password"
                                        type="password"
                                        onChange={handleChange} onBlur={handleBlur}
                                        value={values.password}
                                    />
                                    {errors.password &&
                                    touched.password &&
                                    <Label pointing>{errors.password}</Label>}
                                </Form.Field>
                                <Button.Submit color="violet" fluid size="large" type="submit" loading={loading}>
                                    Submit
                                </Button.Submit>

                                {apiError && <Message color="red">
                                    {apiError.response.error_description}
                                </Message>}
                            </Form>
                        </Card.Description>
                    </Card.Content>
                </Card>
            </Grid.Column>}
        </Grid>
    );
};

const UnconnectedLoginPageForm = withFormik({
    handleSubmit: (values, formikBag: FormikBag<ILoginPageProps, IFormValues>) => {
        formikBag.props.login(values.email, values.password);
        formikBag.setSubmitting(false);
    },

    validationSchema: Yup.object().shape({
        email: Yup.string().required("Required"),
        password: Yup.string().required("Required"),
    }),
})(UnconnectedLoginPage);

export const LoginPage = connect(
    (state: RootState) => ({
        access_token: state.auth.access_token,
        apiError: state.auth.error,
        loading: state.auth.loading,
    }),
    {login: actions.login})(UnconnectedLoginPageForm);
