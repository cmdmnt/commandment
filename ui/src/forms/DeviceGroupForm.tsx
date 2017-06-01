import * as React from 'react';
import {Field, reduxForm, FormProps} from 'redux-form';
import {Form, Button} from 'semantic-ui-react';
import {SemanticInput} from "./fields/SemanticInput";

export interface FormData {
    name: string;
}

interface DeviceGroupFormProps extends FormProps<FormData, any, any> {

}

@reduxForm<FormData, DeviceGroupFormProps, undefined>({
    form: 'device_group'
})
export class DeviceGroupForm extends React.Component<DeviceGroupFormProps, undefined> {
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