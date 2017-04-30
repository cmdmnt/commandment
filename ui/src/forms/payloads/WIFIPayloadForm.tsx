import * as React from 'react';
import {Field, reduxForm, FormProps, formValueSelector, FormSection} from 'redux-form';
import {connect} from "react-redux";
import {ProxyDetails, WIFIProxyType} from "./WIFIPayload/ProxyDetails";
import {EAPClientConfiguration} from "./WIFIPayload/EAPClientConfiguration";

export type WIFIEncryptionType = 'None' | 'Any' | 'WPA2' | 'WPA' | 'WEP';


export interface EAPClientConfiguration {
    username?: string;
    accept_eap_types: Array<number>;
    user_password?: string;
    one_time_password?: boolean;
    payload_certificate_anchor_uuid?: Array<string>;
    tls_trusted_server_names?: Array<string>;
    tls_allow_trust_exceptions?: boolean;
    tls_certificate_is_required?: boolean;
    outer_identity?: string;
    ttls_inner_authentication?: string;
    eap_fast_use_pac?: boolean;
    eap_fast_provision_pac?: boolean;
    eap_fast_provision_pac_anonymously?: boolean;
    eap_sim_number_of_rands?: number;
    system_mode_credentials_source?: 'ActiveDirectory';
}

export interface QoSMarkingPolicy {
    qos_marking_whitelisted_app_identifiers: Array<string>;
    qos_marking_apple_audio_video_calls: boolean;
    qos_marking_enabled: boolean;
}

export interface WIFIPayload {
    ssid_str?: string;
    hidden_network: boolean;
    auto_join?: boolean;
    encryption_type: WIFIEncryptionType;

    // HotSpot
    is_hotspot?: boolean;
    domain_name?: string;
    service_provider_roaming_enabled?: boolean;
    roaming_consortium_ois?: Array<string>;
    nai_realm_names?: Array<string>;
    mcc_and_mncs?: Array<string>;
    displayed_operator_name?: string;
    proxy_type?: WIFIProxyType;
    captive_bypass?: boolean;
    qos_marking_policy?: QoSMarkingPolicy;

    password?: string;
    eap_client_configuration?: EAPClientConfiguration;
    payload_certificate_uuid?: string;

    // Proxy
    proxy_server?: string;
    proxy_server_port?: number;
    proxy_username?: string;
    proxy_password?: string;
    proxy_pac_url?: string;
    proxy_pac_fallback_allowed?: boolean;
}

interface WIFIPayloadFormProps extends FormProps<WIFIPayload, any, any> {
    is_hotspot: boolean;
}

const selector = formValueSelector('wifi_payload');

@connect(
    state => {
        const is_hotspot = selector(state, 'is_hotspot');
        return {
            is_hotspot
        }
    }
)
@reduxForm<WIFIPayload, WIFIPayloadFormProps, undefined>({
    form: 'wifi_payload'
})
export class WIFIPayloadForm extends React.Component<WIFIPayloadFormProps, undefined> {

    render() {
        const {
            is_hotspot
        } = this.props;
        
        return (
            <form>
                <div className='row'>
                    <div className='column'>
                        <label htmlFor='ssid-str'>SSID</label>
                        <Field id='ssid-str' name='ssid_str' component='input' type='text' required />
                    </div>
                    <div className='column-20'>

                        <label htmlFor='is-hidden'>Hidden
                            <Field id='is-hidden' name='is_hidden' component='input' type='checkbox' value={true} />
                        </label>
                    </div>
                </div>
                <div className='row'>
                    <div className='column'>
                        <Field id='auto-join' name='auto_join' component='input' type='checkbox' value={true} />
                        <label className='label-inline' htmlFor='auto-join'>Auto Join</label>
                    </div>
                </div>
                <div className='row'>
                    <div className='column'>
                        <label htmlFor='encryption-type'>Encryption</label>
                        <Field id='encryption-type' name='encryption_type' component='select'>
                            <option value='None'>None</option>
                            <option value='Any'>Any</option>
                            <option value='WPA2'>WPA2</option>
                            <option value='WPA'>WPA</option>
                            <option value='WEP'>WEP</option>
                        </Field>
                    </div>
                </div>
                <div className='row'>
                    <div className='column'>
                        <Field id='is-hotspot' name='is_hotspot' component='input' type='checkbox' value={true} />
                        <label className='label-inline' htmlFor='is-hotspot'>HotSpot</label>
                    </div>
                </div>
                {is_hotspot && <fieldset name='hotspot'>
                    <div className='row'>
                        <div className='column'>
                            <label htmlFor='domain-name'>Domain Name</label>
                            <Field id='domain-name' name='domain_name' component='input' type='text' />
                        </div>
                    </div>
                    <div className='row'>
                        <div className='column'>
                            <Field
                                id='service-provider-roaming-enabled'
                                name='service_provider_roaming_enabled'
                                component='input'
                                type='checkbox'
                                value={true} />
                            <label className='label-inline' htmlFor='service-provider-roaming-enabled'>Service Provider Roaming Enabled</label>
                        </div>
                    </div>
                    <div className='row'>
                        <div className='column'>
                            <label htmlFor='displayed-operator-name'>Displayed Operator Name</label>
                            <Field
                                id='displayed-operator-name'
                                name='displayed_operator_name'
                                component='input'
                                type='text' />
                        </div>
                    </div>
                </fieldset>}

                <div className='row'>
                    <div className='column'>
                        <Field id='captive-bypass' name='captive_bypass' component='input' type='checkbox' value={true} />
                        <label className='label-inline' htmlFor='captive-bypass'>Captive Bypass</label>
                    </div>
                </div>
                <div className='row'>
                    <div className='column'>
                        <label htmlFor='password'>Password</label>
                        <Field id='password' name='password' component='input' type='password' />
                    </div>
                </div>
                <FormSection name='proxy'>
                    <ProxyDetails/>
                </FormSection>
                <FormSection name='eap_client_configuration'>
                    <EAPClientConfiguration/>
                </FormSection>
            </form>
        )
    }
}

