import * as React from 'react';
import {Field, reduxForm, FormProps} from 'redux-form';

export interface FormData {
    allow_all_apps_access: boolean;
    cert_server: string;
    cert_template: string;
    certificate_acquisition_mechanism: 'RPC' | 'HTTP';
    certificate_authority: string;
    certificate_renewal_time_interval: number;
    description: string;
    key_is_extractable: boolean;
    prompt_for_credentials?: boolean;
    keysize?: number;
}

interface ADCertPayloadFormProps extends FormProps<FormData, any, any> {

}

@reduxForm<FormData, ADCertPayloadFormProps, undefined>({
    form: 'ad_cert_payload'
})
export class ADCertPayloadForm extends React.Component<ADCertPayloadFormProps, undefined> {
    render() {
        const {
            handleSubmit
        } = this.props;

        return (
            <form onSubmit={handleSubmit}>
                <div className='row'>
                    <div className='column'>
                        <label>
                            <Field name='allow_all_apps_access' component='input' type='checkbox' value='1' />
                            <span className='label-inline'>Apps have access to the private key</span>
                        </label>

                        <label htmlFor='cert_server'>Active Directory CA Host name</label>
                        <Field id='cert_server' name='cert_server' component='input' required />

                        <label htmlFor='cert_template'>Template name</label>
                        <Field id='cert_template' name='cert_template' component='input' required />

                        <label htmlFor='certificate_acquisition_mechanism'>Acquisition mechanism</label>
                        <Field
                            id='certificate_acquisition_mechanism'
                            component='select'
                            name='certificate_acquisition_mechanism'
                        >
                            <option value='RPC'>RPC</option>
                            <option value='HTTP'>HTTP</option>
                        </Field>

                        <label htmlFor='certificate_authority'>Certificate authority name</label>
                        <Field id='certificate_authority' name='certificate_authority' component='input' required />

                        <label htmlFor='certificate_renewal_time_interval'>Renewal interval</label>
                        <Field
                            id='certificate_renewal_time_interval'
                            name='certificate_renewal_time_interval'
                            component='input'
                            type='number'
                            required />
                        <span className='label-inline'>Day(s)</span>
                        
                        <label htmlFor='description'>Description</label>
                        <Field id='description' name='description' component='input' />

                        <label>
                            <Field name='key_is_extractable' component='input' type='checkbox' value='1' />
                            <span className='label-inline'>Private key is extractable</span>
                        </label>

                        <label>
                            <Field name='prompt_for_credentials' component='input' type='checkbox' value='1' />
                            <span className='label-inline'>Prompt for credentials (manual only)</span>
                        </label>

                        <label htmlFor='keysize'>Key size</label>
                        <Field id='keysize' name='keysize' component='input' />
                    </div>
                </div>
            </form>
        )
    }
}