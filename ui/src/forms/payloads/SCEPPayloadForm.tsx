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
                        <Field id='url' name='url' component='input' type='url' placeholder='http://scep.example.com/scep' required />
                         <span>Test will send a GetCACaps message</span>
                    </div>
                    <div className='column-30'>
                        <button className="button button-outline form-field-button">Test</button>
                    </div>
                </div>
                <div className='row'>
                    <div className='column'>
                        <label htmlFor='name'>Name</label>
                        <Field id='name' name='name' component='input' type='text' placeholder='(Optional) CA-NAME or organization.org' />
                        <p>Any string that is understood by the SCEP server.</p>

                        <label htmlFor='subject'>Subject</label>
                        <Field id='subject' name='subject' component='input' type='text' placeholder='O=Commandment/OU=IT/CN=%HardwareUUID%' />

                    </div>
                </div>
                <div className='row'>
                    <div className='column'>
                        <label htmlFor='challenge'>Challenge</label>
                        <Field id='challenge' name='challenge' component='input' type='password' />


                    </div>
                    <div className='column'>

                        <label htmlFor='challenge'>Confirm Challenge</label>
                        <Field id='confirm_challenge' name='confirm_challenge' component='input' type='password' />
                    </div>
                </div>
                <div className='row'>
                    <div className='column'>
                        <p>Optional. Used as the pre-shared secret for automatic enrollment</p>
                        
                        <label htmlFor='key_size'>Key size (in bits)</label>
                        <Field id='key_size_1024' component='input' type='radio' name='key_size' value='1024' /><label className='label-inline' htmlFor='key_size_1024'>1024</label>
                        <Field id='key_size_2048' component='input' type='radio' name='key_size' value='2048' /><label className='label-inline' htmlFor='key_size_2048'>2048</label>

                    </div>
                </div>
                <div className='row'>
                    <div className='column'>
                        <label htmlFor='ca_fingerprint'>CA Fingerprint</label>
                        <Field id='ca_fingerprint' name='ca_fingerprint' component='input' type='text' />
                    </div>
                    <div className='column-30'>
                        Upload
                    </div>
                </div>
                <div className='row'>
                    <div className='column'>
                        <h4>Use SCEP key for</h4>

                        <Field id='key_usage_signing' name='key_usage_signing' component='input' type='checkbox' value='1' />
                        <label className='label-inline' htmlFor='key_usage_signing'>Signing</label>

                        <Field id='key_usage_encryption' name='key_usage_encryption' component='input' type='checkbox' value='4' />
                        <label className='label-inline' htmlFor='key_usage_encryption'>Encryption</label>

                        <label htmlFor='subject_alt_name'>SubjectAltName</label>
                        <Field id='subject_alt_name' name='subject_alt_name' component='input' type='text' />

                    </div>
                </div>
                <div className='row'>
                    <div className='column'>
                        <label htmlFor='retries'>Retries</label>
                        <Field id='retries' name='retries' component='input' type='number' />
                        <p>The number of times the device should retry if the server sends a PENDING response</p>
                    </div>
                    <div className='column'>
                        <label htmlFor='retry_delay'>Retry Delay</label>
                        <Field id='retry_delay' name='retry_delay' component='input' type='number' />
                        <p>The number of seconds to wait between subsequent retries. The first retry is attempted without this delay</p>
                    </div>
                </div>
                <div className='row'>
                    <div className='column'>
                        <button type="submit">Submit</button>
                    </div>
                </div>
            </form>
        );
    }
}
