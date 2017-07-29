import * as React from 'react';
import {Field, reduxForm, FormProps} from 'redux-form';

export interface FormData {

}

interface APNSConfigurationFormProps extends FormProps<FormData, any, any> {

}

@reduxForm({
    form: 'apns_configuration'
})
export class APNSConfigurationForm extends React.Component<APNSConfigurationFormProps, undefined> {
    render() {
        const {
            handleSubmit
        } = this.props;

        return (
            <form onSubmit={handleSubmit}>
            </form>
        );
    }
}
