import * as React from 'react';
import {Field, reduxForm, FormProps} from 'redux-form';

export interface FormData {
    scep_type: 'internal' | 'external';
    scep_url: string;
}

interface SCEPConfigurationFormProps extends FormProps<FormData, any, any> {

}

@reduxForm({
    form: 'scep_configuration'
})
export class SCEPConfigurationForm extends React.Component<SCEPConfigurationFormProps, undefined> {
    render() {
        const {
            handleSubmit
        } = this.props;

        return (
            <form onSubmit={handleSubmit}>
                <fieldset>
                    <label>
                        <Field name='scep_type' component='input' type='radio' value='internal'/>
                        <span className="label-inline">Use internal SCEP service</span>
                    </label>
                    <p>Your devices will contact this server directly to request their identity certificate.</p>
                    <p>Use this if you are testing or developing commandment.</p>
                </fieldset>
                <fieldset>
                    <label>
                        <Field name='scep_type' component='input' type='radio' value='external'/>
                        <span className="label-inline">Use external SCEP service</span>
                    </label>
                    <p>Devices will contact an external service to request their identity certificate.</p>

                    <div className='row'>
                        <div className='column'>
                            <label htmlFor='scepUrl'>URL</label>
                            <Field id='scepUrl' name='scep_url' component='input' type='text'
                                   placeholder='eg. http://scep.example.com/scep'/>
                        </div>
                        <div className='column column-20'>
                            <button className="button button-outline form-field-button">Test</button>
                        </div>
                    </div>

                    <label htmlFor='scepChallenge'>Challenge</label>
                    <Field id='scepChallenge' name='scep_challenge' component='input' type='password'/>

                    <label htmlFor='scepChallengeConfirm'>Challenge (Confirm)</label>
                    <Field id='scepChallengeConfirm' name='scep_challenge_confirm' component='input' type='password'/>

                    <label htmlFor='scepSubject'>Request Subject</label>
                    <Field id='scepSubject' name='scep_subject' component='input' type='text'/>

                    <em>NOTE:</em> The following variables are substituted when a macOS client makes a SCEP request:
                    <blockquote>
                        %AD_ComputerID%, %AD_ComputerName%, %AD_Domain%, %AD_DomainForestName%, %AD_DomainGUID%,
                        %AD_DomainNameDNS%, %AD_KerberosID%, %ComputerName%, %HardwareUUID%, %HostName%,
                        %LocalHostName%, %MACAddress%, %SerialNumber%
                    </blockquote>

                    <input className="button-primary" type="submit" value="Save"/>
                </fieldset>
            </form>
        )
    }
}