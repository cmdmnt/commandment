import * as React from 'react';
import {Field, formValueSelector} from 'redux-form';
import {connect} from "react-redux";
import {RootState} from "../../../reducers/index";

enum EAPType {
    TLS = 13,
    LEAP = 17,
    EAPSIM = 18,
    TTLS = 21,
    EAPAKA = 23,
    PEAP = 25,
    EAPFAST = 43
}

export type TTLSInnerAuthentication = 'PAP' | 'CHAP' | 'MSCHAP' | 'MSCHAPv2' | 'EA';

export interface EAPClientConfiguration {
    username?: string;
    accept_eap_types: Array<EAPType>;
    user_password?: string;
    one_time_password?: boolean;
    payload_certificate_anchor_uuid?: Array<string>;
    tls_trusted_server_names?: Array<string>;
    tls_allow_trust_exceptions?: boolean;
    tls_certificate_is_required?: boolean;
    outer_identity?: string;
    ttls_inner_authentication?: TTLSInnerAuthentication;
    eap_fast_use_pac?: boolean;
    eap_fast_provision_pac?: boolean;
    eap_fast_provision_pac_anonymously?: boolean;
    eap_sim_number_of_rands?: number;
    system_mode_credentials_source?: 'ActiveDirectory';
}

const selector = formValueSelector('wifi_payload');

interface EAPClientConfigurationProps {
    accept_eap_types: { [eapType: number]: boolean };
}

function mapStateToProps(state): EAPClientConfigurationProps {
    const accept_eap_types = selector(state, 'eap_client_configuration.accept_eap_types');
    
    return {
        accept_eap_types
    }
}

@connect(
    mapStateToProps
)
export class EAPClientConfiguration extends React.Component<EAPClientConfigurationProps, undefined> {
    render() {
        const {
            accept_eap_types
        } = this.props;

        return (
            <fieldset name='eap_client_configuration'>
                <legend><h3><span className='fa fa-building' />Enterprise (802.1x) Profile Configuration</h3></legend>
                <div className='row'>
                    <div className='column'>
                        <h4>Accept EAP Types</h4>

                        <Field id='eap-type-tls' name={`accept_eap_types[${EAPType.TLS}]`} component='input'
                               type='checkbox' value={true} />
                        <label className='label-inline' htmlFor='eap-type-tls'>TLS</label>

                        <Field id='eap-type-leap' name={`accept_eap_types[${EAPType.LEAP}]`} component='input'
                               type='checkbox' value={true} />
                        <label className='label-inline' htmlFor='eap-type-leap'>LEAP</label>

                        <Field id='eap-type-eapsim' name={`accept_eap_types[${EAPType.EAPSIM}]`} component='input'
                               type='checkbox' value={true} />
                        <label className='label-inline' htmlFor='eap-type-eapsim'>EAP-SIM</label>

                        <Field id='eap-type-ttls' name={`accept_eap_types[${EAPType.TTLS}]`} component='input'
                               type='checkbox' value={true} />
                        <label className='label-inline' htmlFor='eap-type-ttls'>TTLS</label>

                        <Field id='eap-type-eapaka' name={`accept_eap_types[${EAPType.EAPAKA}]`} component='input'
                               type='checkbox' value={true} />
                        <label className='label-inline' htmlFor='eap-type-eapaka'>EAP-AKA</label>

                        <Field id='eap-type-peap' name={`accept_eap_types[${EAPType.PEAP}]`} component='input'
                               type='checkbox' value={true} />
                        <label className='label-inline' htmlFor='eap-type-peap'>PEAP</label>

                        <Field id='eap-type-eapfast' name={`accept_eap_types[${EAPType.EAPFAST}]`} component='input'
                               type='checkbox' value={true} />
                        <label className='label-inline' htmlFor='eap-type-eapfast'>EAP-FAST</label>
                    </div>
                </div>
                <div className='row'>
                    <div className='column'>
                        <label htmlFor='username'>Username</label>
                        <Field id='username' name='username' component='input' type='text' />
                    </div>
                    <div className='column'>
                        <label htmlFor='user_password'>Password</label>
                        <Field id='user-password' name='user_password' component='input' type='password' />
                    </div>
                </div>
                <div className='row'>
                    <div className='column'>
                        <label htmlFor='one-time-password'>One Time Password</label>
                        <Field id='one-time-password' name='one_time_password' component='input' type='checkbox' value={true} />
                    </div>
                </div>
                <div className='row'>
                    <div className='column'>
                        <Field id='tls-allow-trust-exceptions' name='tls_allow_trust_exceptions' component='input'
                               type='checkbox' value={true} />
                        <label className='label-inline' htmlFor='tls-allow-trust-exceptions'>Allow Trust Exceptions</label>
                    </div>
                </div>
                <div className='row'>
                    <div className='column'>
                        <Field id='tls-certificate-is-required' name='tls_certificate_is_required' component='input'
                               type='checkbox' value={true} />
                        <label className='label-inline' htmlFor='tls-certificate-is-required'>Allow Two Factor Authentication</label>
                    </div>
                </div>
                {accept_eap_types && (accept_eap_types[EAPType.TTLS] || accept_eap_types[EAPType.PEAP] || accept_eap_types[EAPType.EAPFAST]) &&
                <div className='row'>
                    <div className='column'>
                        <label htmlFor='outer-identity'>Outer Identity</label>
                        <Field id='outer-identity' name='outer_identity' component='input' type='text' />
                    </div>
                </div>}
                {accept_eap_types && accept_eap_types[EAPType.TTLS] &&
                <div className='row'>
                    <div className='column'>
                        <label htmlFor='ttls-inner-authentication'>TTLS Inner Authentication</label>
                        <Field id='ttls-inner-authentication' name='ttls_inner_authentication' component='select'>
                            <option value='PAP'>PAP</option>
                            <option value='CHAP'>CHAP</option>
                            <option value='MSCHAP'>MSCHAP</option>
                            <option value='MSCHAPv2'>MSCHAPv2</option>
                            <option value='EA'>EA</option>
                        </Field>
                    </div>
                </div>}
            </fieldset>
        )
    }
}