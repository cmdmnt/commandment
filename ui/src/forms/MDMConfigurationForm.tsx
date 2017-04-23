import * as React from 'react';
import {Field, reduxForm, FormProps} from 'redux-form';

export interface FormData {
    prefix: string;
    addl_config: any;
    topic: string;
    access_rights: number;
    mdm_url: string;
    checkin_url: string;
    mdm_name: string;
    description: string;
    ca_cert_id: number;
    push_cert_id: number;
    device_identity_method: string;
    scep_url: string;
    scep_challenge: string;
}

interface MDMConfigurationFormProps extends FormProps<FormData, any, any> {
    CACertificate?: JSONAPIDetailResponse<Certificate, undefined>;
    PushCertificate?: JSONAPIDetailResponse<Certificate, undefined>;
}

@reduxForm<FormData, MDMConfigurationFormProps>({
    form: 'mdm_configuration'
})
export class MDMConfigurationForm extends React.Component<MDMConfigurationFormProps, undefined> {

    static defaultProps: MDMConfigurationFormProps = {
    };


    render(): JSX.Element {
        const {
            handleSubmit,
            CACertificate,
            PushCertificate
        } = this.props;

        return (
            <form onSubmit={handleSubmit}>
                <fieldset>
                    <label htmlFor='prefix'>Prefix</label>
                    <Field name='prefix' component='input' type='text' placeholder='' id='prefix' />
                    <span>The prefix is the reverse style DNS name of your organization</span>

                    <label htmlFor='topic'>Push Topic</label>
                    <Field name='topic' component='input' type='text' id='topic' placeholder='Calculated from push certificate' disabled />

                    <label htmlFor='mdm_url'>MDM URL</label>
                    <Field name='mdm_url' component='input' type='text' id='mdm_url' />

                    <label htmlFor='checkin_url'>Checkin URL</label>
                    <Field name='checkin_url' component='input' type='text' id='checkin_url' />

                    <label htmlFor='ca_cert_id'>CA Certificate</label>
                    <Field name='ca_cert_id' component='select' id='ca_cert_id'>
                        {CACertificate && <option value={CACertificate.data.id}>{CACertificate.data.attributes.x509_cn}</option>}
                    </Field>

                    <label htmlFor='push_cert_id'>Push Certificate</label>
                    <Field name='push_cert_id' component='select' id='push_cert_id'>
                        {PushCertificate && <option value={PushCertificate.data.id}>{PushCertificate.data.attributes.x509_cn}</option>}
                    </Field>

                    <label>
                        Device Identity Certificates
                        <br />

                        <Field id='device_identity_provision' name='device_identity_method' component='input' type='radio' value='provision' />
                        <span className="label-inline">Generate device certificates</span>
                        <Field id='device_identity_scep' name='device_identity_method' component='input' type='radio' value='scep' />
                        <span className="label-inline">Use external SCEP service</span>
                        <Field id='device_identity_ourscep' name='device_identity_method' component='input' type='radio' value='ourscep' />
                        <span className="label-inline">Use internal SCEP service</span>
                    </label>

                    <div className='row'>
                        <div className='column'>
                            <label htmlFor='scep_url'>SCEP URL</label>
                            <Field name='scep_url' component='input' type='text' id='scep_url' />
                        </div>
                        <div className='column'>
                            <label htmlFor='scep_challenge'>SCEP Challenge</label>
                            <Field name='scep_challenge' component='input' type='text' id='scep_challenge' />
                        </div>
                    </div>
                </fieldset>
            </form>
        );
    }
}
