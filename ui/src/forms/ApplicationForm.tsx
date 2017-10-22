import * as React from 'react';
import {Field, reduxForm, FormProps} from 'redux-form';
import {Form, Button} from 'semantic-ui-react';
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
                <Field id='name' label='Name' name='name' component={SemanticInput} type='text' required />
                <Button type='submit'>Save</Button>
            </Form>
        );
    }
}

export const ApplicationForm = reduxForm<FormData, ApplicationFormProps, undefined>({
    form: 'application'
})(UnconnectedApplicationForm);