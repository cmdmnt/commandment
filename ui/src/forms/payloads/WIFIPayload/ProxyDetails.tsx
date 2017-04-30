import * as React from 'react';
import {connect} from 'react-redux';
import {Field, FormState, formValueSelector} from 'redux-form';
export type WIFIProxyType = 'None' | 'Manual' | 'Auto';

const selector = formValueSelector('wifi_payload');

interface ProxyDetailsProps {
    proxy_type: WIFIProxyType;
}

function mapStateToProps(state: FormState): ProxyDetailsProps {
    const proxy_type = selector(state, 'proxy.proxy_type');
    return {
        proxy_type
    }
}

@connect(
    mapStateToProps
)
export class ProxyDetails extends React.Component<ProxyDetailsProps, undefined> {
    render() {
        const {
            proxy_type
        } = this.props;

        return (
            <fieldset name='proxy'>
                <legend><h3>Proxy</h3></legend>
                <div className='row'>
                    <div className='column'>
                        <Field id='proxy-type-none' name='proxy_type' component='input' type='radio' value='None' />
                        <label className='label-inline' htmlFor='proxy-type-none'>None</label>

                        <Field id='proxy-type-manual' name='proxy_type' component='input' type='radio' value='Manual' />
                        <label className='label-inline' htmlFor='proxy-type-manual'>Manual</label>

                        <Field id='proxy-type-auto' name='proxy_type' component='input' type='radio' value='Auto' />
                        <label className='label-inline' htmlFor='proxy-type-auto'>Auto</label>
                    </div>
                </div>
                {proxy_type && proxy_type !== 'None' &&
                <div>
                    <div className='row'>
                        <div className='column'>
                            <label htmlFor='proxy-server'>Proxy Address</label>
                            <Field id='proxy-server' name='proxy_server' component='input' type='text'/>
                        </div>
                        <div className='column column-20'>
                            <label htmlFor='proxy-server-port'>Port</label>
                            <Field id='proxy-server-port' name='proxy_server_port' component='input' type='number'/>
                        </div>
                    </div>
                    <div className='row'>
                        <div className='column'>
                            <label htmlFor='proxy-username'>Username</label>
                            <Field id='proxy-username' name='proxy_username' component='input' type='text'/>
                        </div>
                        <div className='column'>
                            <label htmlFor='proxy-password'>Password</label>
                            <Field id='proxy-password' name='proxy_password' component='input' type='password'/>
                        </div>
                    </div>
                    <div className='row'>
                        <div className='column'>
                            <span className='float-right'>If empty will use WPAD</span>
                            <label htmlFor='proxy-pac-url'>PAC URL</label>
                            <Field id='proxy-pac-url' name='proxy_pac_url' component='input' type='text'/>
                        </div>
                        <div className='column-20'>
                            <label htmlFor='proxy-pac-fallback-allowed'>Fallback
                                Allowed</label>
                            <Field id='proxy-pac-fallback-allowed' name='proxy_pac_fallback_allowed' component='input'
                                   type='checkbox' value={true}/>
                        </div>
                    </div>
                </div>}
            </fieldset>
        )
    }
}