import * as React from 'react';
import {Field, reduxForm, FormProps} from 'redux-form';
import {Header, Icon, Segment, Message, Input, Button, Grid, Form, Radio} from 'semantic-ui-react';
import {SemanticInput} from "./fields/SemanticInput";
import {SemanticTextArea} from "./fields/SemanticTextArea";

export interface FormData {
    display_name: string;
    description: string;
    manifest_url: string;
}

interface ApplicationFormProps extends FormProps<FormData, any, any> {

}

const UnconnectedApplicationForm: React.StatelessComponent<ApplicationFormProps> = props => {
        const { error, handleSubmit, pristine, reset, submitting } = props;

        return (
            <Form onSubmit={handleSubmit}>
                <Message attached>Enterprise Application</Message>
                <Segment attached>
                    <Field
                        id='display-name'
                        label='Display Name'
                        name='display_name'
                        component={SemanticInput}
                        type='text' required />
                    <Field
                        id='description'
                        label='Description'
                        name='description'
                        component={SemanticTextArea}
                        type='TextArea' />
                    <Field
                        id='manifest-url'
                        label='Manifest URL'
                        name='manifest_url'
                        component={SemanticInput}
                        type='text' />
                    {error && <strong>{error}</strong>}
                    <Button type='submit' disabled={submitting}>Save</Button>
                </Segment>
            </Form>
        );
};

export const ApplicationForm = reduxForm<FormData, ApplicationFormProps, undefined>({
    form: 'application'
})(UnconnectedApplicationForm);
