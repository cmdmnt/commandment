import * as React from 'react';
import {Field, reduxForm, FormProps} from 'redux-form';

export interface FormData {
    scep_type: 'internal' | 'external';
    scep_url: string;
}

interface CAConfigurationFormProps extends FormProps<FormData, any, any> {

}

@reduxForm<FormData, CAConfigurationFormProps, undefined>({
    form: 'ca_configuration'
})
export class CAConfigurationForm extends React.Component<CAConfigurationFormProps, undefined> {
    render() {
        const {
            handleSubmit
        } = this.props;

        return (
            <form onSubmit={handleSubmit}>
                <div className='row'>
                    <div className='column'>
                        <label>
                            <Field name='scep_type' component='input' type='radio' value='internal'/>
                            <span className="label-inline">Use internal SCEP service</span>
                        </label>
                        <p>Your devices will contact this server directly to request their identity certificate.
                    Use this if you are testing or developing commandment.</p>
                    </div>
                    <div className='column'>
                        <label>
                            <Field name='scep_type' component='input' type='radio' value='external'/>
                            <span className="label-inline">Use external SCEP service</span>
                        </label>
                        <p>Devices will contact an external service to request their identity certificate.</p>
                    </div>
                </div>
                <fieldset>
                    <hr />

                    <div className='row'>
                        <div className='column'>
                            <label htmlFor='scepUrl'>URL</label>
                            <Field id='scepUrl' name='scep_url' component='input' type='text'
                                   placeholder='eg. http://scep.example.com/scep'/>
                            <div className='float-right'>
                                <button className="button button-outline">Test</button>
                            </div>
                        </div>
                    </div>
                    <div className='row'>
                        <div className='column'>
                            <label htmlFor='scepChallenge'>Challenge</label>
                            <Field id='scepChallenge' name='scep_challenge' component='input' type='password'/>
                        </div>
                        <div className='column'>
                            <label htmlFor='scepChallengeConfirm'>Challenge (Confirm)</label>
                            <Field id='scepChallengeConfirm' name='scep_challenge_confirm' component='input' type='password'/>
                        </div>
                    </div>

                    <label htmlFor='scepSubject'>SCEP Client Certificate Name</label>
                    <Field name='scepSubject' component='select' id='scepSubject'>
                        <option value='%HardwareUUID%'>%HardwareUUID% - The hardware UDID</option>
                        <option value='%HostName%'>%HostName% - The local hostname eg. (joe.local)</option>
                        <option value='%LocalHostName%'>%LocalHostName% - The hostname without the .local suffix</option>
                        <option value='%MACAddress%'>%MACAddress% - Active ethernet interface MAC address</option>
                        <option value='%SerialNumber%'>%SerialNumber% - Serial number of the device</option>
                    </Field>

                    <input className="button-primary" type="submit" value="Save"/>
                </fieldset>
            </form>
        )
    }
}