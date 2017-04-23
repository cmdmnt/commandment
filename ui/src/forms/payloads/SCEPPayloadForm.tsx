import * as React from 'react';
import {Field, reduxForm, FormProps} from 'redux-form';


export interface FormData {
    id?: string;
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
    onClickTest: (url: string) => void;
}

@reduxForm<FormData, SCEPPayloadFormProps, undefined>({
    form: 'scep_payload'
})
export class SCEPPayloadForm extends React.Component<SCEPPayloadFormProps, undefined> {
    handleClickTest = (e: any) => {
        e.preventDefault();
        // TODO: dispatch test action
    };

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
                    </div>
                    <div className='column-30 column-bottom'>
                        <button className="button button-outline form-field-button" onClick={this.handleClickTest}>Test + Fingerprint</button>
                    </div>
                </div>
                <div className='row'>
                    <div className='column'>
                        <label htmlFor='cafingerprint'>CA Fingerprint <small className='float-right'>A fingerprint ensures your devices trust this server only</small></label>
                        <Field id='cafingerprint' name='ca_fingerprint' component='input' type='text' />
                    </div>
                </div>
                <div className='row'>
                    <div className='column'>
                        <label htmlFor='name'>Name <small className='float-right'>Optional. Any string that is understood by the SCEP server.</small></label>
                        <Field id='name' name='name' component='input' type='text' placeholder='CA-NAME or organization.org' />
        

                        <label htmlFor='subject'>Subject</label>
                        <Field id='subject' name='subject' component='input' type='text' placeholder='O=Commandment/OU=IT/CN=%HardwareUUID%' />

                    </div>
                </div>
                <div className='row'>
                    <div className='column'>
                        <label htmlFor='challenge'>Challenge <small className='float-right'>Optional. Used as the pre-shared secret for automatic enrollment</small></label>
                        <Field id='challenge' name='challenge' component='input' type='password' />
                    </div>
                </div>
                <div className='row'>
                    <div className='column'>
                        <h4>Key size (in bits)</h4>
                        <label>
                            <Field id='key_size_1024' component='input' type='radio' name='key_size' value='1024' />
                            <span className='label-inline'>1024</span>
                        </label>
                        <label>
                            <Field id='key_size_2048' component='input' type='radio' name='key_size' value='2048' />
                            <span className='label-inline'>2048</span>
                        </label>
                    </div>
                    <div className='column'>
                        <h4>Use SCEP key for</h4>

                        <label>
                            <Field id='key_usage_signing' name='key_usage_signing' component='input' type='checkbox' value='1' />
                            <span className='label-inline' >Signing</span>
                        </label>

                        <label>
                            <Field id='key_usage_encryption' name='key_usage_encryption' component='input' type='checkbox' value='4' />
                            <span className='label-inline'>Encryption</span>
                        </label>
                    </div>
                </div>
                <div className='row'>
                    <div className='column'>


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
