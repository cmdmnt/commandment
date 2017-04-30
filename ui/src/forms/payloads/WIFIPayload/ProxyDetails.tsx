import * as React from 'react';
import {Field} from 'redux-form';

export class ProxyDetails extends React.Component<undefined, undefined> {
    render() {
        return (
            <fieldset name='proxy'>
                <div className='row'>
                    <div className='column'>
                        <label htmlFor='proxy-type'>Proxy Type</label>
                        <Field id='proxy-type' name='proxy_type' component='select'>
                            <option value='None'>None</option>
                            <option value='Manual'>Manual</option>
                            <option value='Auto'>Auto</option>
                        </Field>
                    </div>
                </div>
                <div className='row'>
                    <div className='column'>
                        <label htmlFor='proxy-server'>Proxy Address</label>
                        <Field id='proxy-server' name='proxy_server' component='input' type='text' />
                    </div>
                    <div className='column column-20'>
                        <label htmlFor='proxy-server-port'>Port</label>
                        <Field id='proxy-server-port' name='proxy_server_port' component='input' type='number' />
                    </div>
                </div>
                <div className='row'>
                    <div className='column'>
                        <label htmlFor='proxy-username'>Username</label>
                        <Field id='proxy-username' name='proxy_username' component='input' type='text' />
                    </div>
                    <div className='column'>
                        <label htmlFor='proxy-password'>Password</label>
                        <Field id='proxy-password' name='proxy_password' component='input' type='password' />
                    </div>
                </div>
                <div className='row'>
                    <div className='column'>
                        <label htmlFor='proxy-pac-url'>PAC URL</label>
                        <Field id='proxy-pac-url' name='proxy_pac_url' component='input' type='text' />
                    </div>
                </div>
                <div className='row'>
                    <div className='column'>
                        <Field id='proxy-pac-fallback-allowed' name='proxy_pac_fallback_allowed' component='input' type='checkbox' value={true} />
                        <label className='label-inline' htmlFor='proxy-pac-fallback-allowed'>PAC Fallback Allowed</label>
                    </div>
                </div>
            </fieldset>
        )
    }
}