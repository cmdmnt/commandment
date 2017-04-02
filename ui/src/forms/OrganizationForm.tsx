import * as React from 'react';
import {Field, reduxForm, FormProps} from 'redux-form';

import './OrganizationForm.scss';

export interface FormData {
    name: string;
    payload_prefix: string;
    x509_ou: string;
    x509_o: string;
    x509_st: string;
    x509_c: string;
}

interface OrganizationFormProps extends FormProps<FormData, any, any> {

}

@reduxForm<FormData, OrganizationFormProps, undefined>({
    form: 'organization'
})
export class OrganizationForm extends React.Component<OrganizationFormProps, undefined> {
    render() {
        const {
            handleSubmit
        } = this.props;

        return (
            <form onSubmit={handleSubmit}>
                <fieldset>
                    <h4>General Information</h4>
                    <label htmlFor='name'>Name</label>
                    <Field name='name' component='input' type='text' placeholder='Acme Inc.' id='name' />
                    <span>The name of your organization</span>

                    <label htmlFor='payload_prefix'>Prefix</label>
                    <Field name='payload_prefix' component='input' type='text' placeholder='com.acme' id='payload_prefix' />
                    <span>The prefix is the reverse style DNS name of your organization which will uniquely identify profiles</span>
                </fieldset>
                <fieldset>
                    <h4>Certificate Details</h4>
                    <p>These details will be shown on any certificates issued by the MDM</p>

                    <label htmlFor='x509_ou'>Organization Unit or Department</label>
                    <Field name='x509_ou' component='input' type='text' id='x509_ou' maxLength={32} />

                    <label htmlFor='x509_o'>Organization Name</label>
                    <Field name='x509_o' component='input' type='text' id='x509_o' maxLength={64} />

                    <label htmlFor='x509_st'>State or Province</label>
                    <Field name='x509_st' component='input' type='text' id='x509_st' maxLength={128} />

                    <label htmlFor='x509_c'>Country</label>
                    <Field name='x509_c' component='select' id='x509_c_id'>
                        <option value='US'>United States</option>
                        <option value='AU'>Australia</option>
                    </Field>
                </fieldset>
                <input className="button-primary" type="submit" value="Save"/>
            </form>
        )
    }
}