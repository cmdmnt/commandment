import * as React from "react";
import {FunctionComponent} from "react";
import {RouteProps} from "react-router";
import {Button, Card, Checkbox, Form} from "semantic-ui-react";

export interface ILoginPageProps {
    onLogin: (evt: Event) => void;
}

export const LoginPage: FunctionComponent<ILoginPageProps & RouteProps> = ({ onLogin }: ILoginPageProps) => {
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
                        <Button type="submit" onClick={onLogin}>Submit</Button>
                    </Form>
                </Card.Description>
            </Card.Content>
        </Card>
    );
};
