import * as React from 'react';
import {Field, reduxForm, FormProps} from 'redux-form';
import {Header, Icon, Segment, Message, Input, Button, Grid, Form, Radio} from 'semantic-ui-react';
import {SemanticInput} from "../fields/SemanticInput";
import {SemanticField} from "../fields/SemanticField";

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
    loading: boolean;
}

@reduxForm<FormData, SCEPPayloadFormProps, undefined>({
    form: 'scep_payload'
})
export class SCEPPayloadForm extends React.Component<SCEPPayloadFormProps, undefined> {

    static defaultProps = {
        loading: false
    };

    handleClickTest = (e: any) => {
        e.preventDefault();
        // TODO: dispatch test action
    };

    render() {
        const {
            handleSubmit,
            loading
        } = this.props;

        return (
            <Form onSubmit={handleSubmit} loading={loading}>
                    <Field id='url' label='URL' name='url' component={SemanticInput} type='url' placeholder='http://scep.example.com/scep' required width={12} />

                <small className='float-right'>A fingerprint ensures your devices trust this server only</small>
                <Field label='CA Fingerprint' id='cafingerprint' name='ca_fingerprint' component={SemanticInput} type='text' />


                <small className='float-right'>Optional. Any string that is understood by the SCEP server.</small>
                <Field label='Name' id='name' name='name' component={SemanticInput} type='text' placeholder='CA-NAME or organization.org' />

                <Field label='Subject' id='subject' name='subject' component={SemanticInput} type='text' placeholder='O=Commandment/OU=IT/CN=%HardwareUUID%' />
                
                <small className='float-right'>Optional. Used as the pre-shared secret for automatic enrollment</small>
                <Field label='Challenge' id='challenge' name='challenge' component={SemanticInput} type='password' />

                <Form.Group>
                    <label>Key size (in bits)</label>
                    <Field id='key_size_1024' component={SemanticField} control={Radio} type='radio' name='key_size' label='1024' value={1024} />
                    <Field id='key_size_2048' component={SemanticField} control={Radio} type='radio' name='key_size' label='2048' value={2048} />
                </Form.Group>

                <Form.Group>
                    <label>Use SCEP key for</label>
                    <Field id='key_usage_signing' name='key_usage' component={SemanticField} control={Radio} type='radio' value={1} label='Signing' />
                    <Field id='key_usage_encryption' name='key_usage' component={SemanticField} control={Radio} type='radio' value={4} label='Encryption' />
                    <Field id='key_usage_both' name='key_usage' component={SemanticField} control={Radio} type='radio' value={5} label='Both' />
                </Form.Group>
                
                <Field id='subject_alt_name' name='subject_alt_name' component={SemanticInput} label='SubjectAltName' type='text' />


                <Field id='retries' label='Retries' name='retries' component={SemanticInput} type='number' />
                <p>The number of times the device should retry if the server sends a PENDING response</p>

                <Field id='retry_delay' label='Retry Delay' name='retry_delay' component={SemanticInput} type='number' />
                <p>The number of seconds to wait between subsequent retries. The first retry is attempted without this delay</p>

                <Button type="submit">Submit</Button>
            </Form>
        );
    }
}
