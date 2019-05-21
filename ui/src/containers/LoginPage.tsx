import * as React from "react";
import {FunctionComponent} from "react";
import {RouteProps} from "react-router";
import {Button, Card, Checkbox, Form} from "semantic-ui-react";
import {connect} from "react-redux";
import {RootState} from "../reducers";
import {bindActionCreators, Dispatch} from "redux";
import * as actions from "../store/auth/actions";


export interface ILoginPageProps {
    login: (evt: Event) => void;
}

export const UnconnectedLoginPage: FunctionComponent<ILoginPageProps & RouteProps> = ({ login }: ILoginPageProps) => {
    return (
        <Card>
            <Card.Content>
                <Card.Header>Sign in</Card.Header>
                <Card.Description>
                    <Form>
                        <Form.Field>
                            <label>E-mail address</label>
                            <input type="email" placeholder="user@domain.com" />
                        </Form.Field>
                        <Form.Field>
                            <label>Password</label>
                            <input type="password" placeholder="Password" />
                        </Form.Field>
                        <Button type="submit" onClick={() => { login("mosen", "mosen"); }}>Submit</Button>
                    </Form>
                </Card.Description>
            </Card.Content>
        </Card>
    );
};

function mapStateToProps(state: RootState, ownProps?: any): {} {
    return {};
}

interface IReduxDispatchProps {
    login: actions.TokenActionRequest;
}

function mapDispatchToProps(dispatch: Dispatch, ownProps?: any): IReduxDispatchProps {
    return bindActionCreators({
        login: actions.login,
    }, dispatch);
}

export const LoginPage = connect(mapStateToProps, mapDispatchToProps)(UnconnectedLoginPage);
