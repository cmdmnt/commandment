import * as React from 'react';
import {Field, reduxForm, FormProps} from 'redux-form';

export interface FormData {
    url: string;
    name: string;
    subject: string;
    challenge: string;
    key_size: number;
    ca_fingerprint: string;
    key_usage: number;
    subject_alt_name: string;
    retries: number;
    retry_delay: number;
}

interface SCEPPayloadFormProps extends FormProps<FormData, any, any> {

}

@reduxForm<FormData, SCEPPayloadFormProps, undefined>({
    form: 'scep_payload'
})
export class SCEPPayloadForm extends React.Component<SCEPPayloadFormProps, undefined> {
    render() {
        const {
            handleSubmit
        } = this.props;

        return (
            <form onSubmit={handleSubmit}>
                <div className='row'>
                    <div className='column'>
                        <label htmlFor='url'>URL</label>
                        <Field id='url' name='url' component='input' type='url' required />

                        <label htmlFor='name'>Name</label>
                        <Field id='name' name='name' component='input' type='text' placeholder='optional' />
                        <p>Any string that is understood by the SCEP server.</p>

                        <label htmlFor='subject'>Subject</label>
                        <Field id='subject' name='subject' component='input' type='text' />

                        <label htmlFor='challenge'>Challenge</label>
                        <Field id='challenge' name='challenge' component='input' type='password' />
                        <p>Used as the pre-shared secret for automatic enrollment</p>

                        <label htmlFor='key_size'>Key size (in bits)</label>
                        <Field id='key_size' component='select' name='key_size'>
                            <option value='1024'>1024</option>
                            <option value='2048'>2048</option>
                        </Field>

                        <label htmlFor='ca_fingerprint'>CA Fingerprint</label>
                        <Field id='ca_fingerprint' name='ca-fingerprint' component='input' />

                        <label>
                            <Field name='key_usage' component='input' type='checkbox' value='1' />
                            <span className='label-inline'>Signing</span>
                        </label>

                        <label>
                            <Field name='key_usage' component='input' type='checkbox' value='4' />
                            <span className='label-inline'>Encryption</span>
                        </label>
                        
                        <label htmlFor='subject_alt_name'>SubjectAltName</label>
                        <Field id='subject_alt_name' name='subject_alt_name' component='input' type='text' />

                        <label htmlFor='retries'>Retries</label>
                        <Field id='retries' name='retries' component='input' type='number' />

                        <label htmlFor='retry_delay'>Retry Delay</label>
                        <Field id='retry_delay' name='retry_delay' component='input' type='number' />
                    </div>
                </div>
            </form>
        );
    }
}
