import * as React from "react";
import {Field, FormProps, reduxForm} from "redux-form";
import Form, {FormComponent, FormProps} from "semantic-ui-react/src/collections/Form";
import Button from "semantic-ui-react/src/elements/Button";

import {SemanticInput} from "./fields/SemanticInput";

export interface FormData {
    name: string;
}

interface DeviceGroupFormProps extends FormProps<FormData, any, any> {

}

class UnconnectedDeviceGroupForm extends React.Component<DeviceGroupFormProps, undefined> {
    public render() {
        const {
            handleSubmit,
        } = this.props;

        return (
            <Form onSubmit={handleSubmit}>
                <Field id="name" label="Name" name="name" component={SemanticInput} type="text" required />
                <Button type="submit">Save</Button>
            </Form>
        );
    }
}

export const DeviceGroupForm = reduxForm<FormData, DeviceGroupFormProps, undefined>({
    form: "device_group",
})(UnconnectedDeviceGroupForm);
