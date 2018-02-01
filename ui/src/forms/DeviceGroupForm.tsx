import * as React from 'react';
import {Field, reduxForm, FormProps} from 'redux-form';
// import {Form, Button} from 'semantic-ui-react';
import * as Form from 'semantic-ui-react/dist/es/collections/Form';
import * as Button from 'semantic-ui-react/dist/es/elements/Button';
import {SemanticInput} from "./fields/SemanticInput";

export interface FormData {
    name: string;
}

interface DeviceGroupFormProps extends FormProps<FormData, any, any> {

}


class UnconnectedDeviceGroupForm extends React.Component<DeviceGroupFormProps, undefined> {
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

export const DeviceGroupForm = reduxForm<FormData, DeviceGroupFormProps, undefined>({
    form: 'device_group'
})(UnconnectedDeviceGroupForm);