import * as React from 'react';
import {Field, reduxForm, FormProps} from 'redux-form';
import {Header, Icon, Segment, Message, Input, Button, Grid, Form, Radio} from 'semantic-ui-react';
import {SemanticInput} from "./fields/SemanticInput";

export interface FormData {
    name: string;
}

interface ApplicationFormProps extends FormProps<FormData, any, any> {

}


class UnconnectedApplicationForm extends React.Component<ApplicationFormProps, undefined> {
    render() {
        const {
            handleSubmit
        } = this.props;

        return (
            <Form onSubmit={handleSubmit}>
                <Message attached>Enterprise Application</Message>
                <Segment attached>
                    <Field id='display-name' label='Display Name' name='display_name' component={SemanticInput} type='text' required />
                    <Field id='description' label='Description' name='description' component={SemanticInput} type='textarea' />
                    <Field id='manifest-url' label='Manifest URL' name='manifest_url' component={SemanticInput} type='text' />
                    <Button type='submit'>Save</Button>
                </Segment>
            </Form>
        );
    }
}

export const ApplicationForm = reduxForm<FormData, ApplicationFormProps, undefined>({
    form: 'application'
})(UnconnectedApplicationForm);
