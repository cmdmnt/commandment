/// <reference path="../../typings/rc-upload.d.ts"/>
import * as React from 'react';
import * as Upload from 'rc-upload';

interface APNSConfigurationProps {

}

export class APNSConfiguration extends React.Component<APNSConfigurationProps,undefined> {

    handleReady = (): void => {
        console.log('ready');
    };

    handleStart = (): void => {
        console.log('start');
    };

    handleError = (): void => {
        console.log('er');
    };

    handleSuccess = (): void => {
        console.log('success');
    };

    render(): JSX.Element {
        
        return (
            <div className='APNSConfiguration'>
                <div className='reversed padded title'><i className="fa fa-certificate" /> Push Certificate</div>
                <div className='top-margin centered container'>
                    <div className='row'>
                        <div className='column'>
                            <p>The MDM requires a Push Certificate to communicate with devices.</p>
                        </div>
                    </div>
                    <div className='row'>
                        <div className='column'>
                            <h3>Upload a Push Certificate (PEM)</h3>
                            <Upload
                                name='file'
                                accept='application/x-pem-file'
                                action='/api/v1/push.pem'
                                onReady={this.handleReady}
                                onStart={this.handleStart}
                                onError={this.handleError}
                                onSuccess={this.handleSuccess}
                            >
                                <button className='button button-outline'>Upload</button>
                            </Upload>
                        </div>
                        <div className='column column-10 text-middle'>
                            <h3 className='text-middle'>OR</h3>
                        </div>
                        <div className='column'>
                            <h3>Generate CSR</h3>
                            <button className='button button-outline'>Generate</button>
                            <p>
                                a signing request
                            </p>
                        </div>
                    </div>
                </div>
            </div>
        )
    }
}