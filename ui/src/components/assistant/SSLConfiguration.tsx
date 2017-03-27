import * as React from 'react';
import {ApUpload, ApUploadStyle} from 'apeman-react-upload';

interface SSLConfigurationProps {
    onClickGenerateCSR: () => void;
    SSLSigningRequest?: any;
}

export class SSLConfiguration extends React.Component<SSLConfigurationProps,undefined> {

    handleLoaded = (urls: Array<string>) => {
        console.dir(urls);
    };

    handleError = (err: Error) => {
        console.log(err);
    };

    handleGenerateCSR = (event: any): void => {
        event.preventDefault();
        this.props.onClickGenerateCSR();
    };

    render() {
        const {
            SSLSigningRequest
        } = this.props;

        return (
            <div className='SSLConfiguration'>
                <div className='reversed padded title'><i className="fa fa-certificate" /> Web Certificate</div>
                <div className='top-margin centered container'>
                    <div className='row'>
                        <div className='column'>
                            <p>You need to generate an SSL Certificate to encrypt communications between the device and
                            the MDM</p>
                        </div>
                    </div>
                    <div className='row'>
                        <div className='column'>
                            <h3>Upload an SSL Certificate</h3>
                            <ApUpload multiple={ false }
                                      id="apns-certificate-upload"
                                      name="apns-certificate-upload-input"
                                      accept="application/x-pkcs12"
                                      onLoad={ this.handleLoaded }
                                      onError={ this.handleError }
                                      text='Upload a PKCS#12 (.p12) File'
                            />
                        </div>
                        <div className='column column-10 text-middle'>
                            <h3 className='text-middle'>OR</h3>
                        </div>
                        <div className='column'>
                            <button className='button button-outline' onClick={this.handleGenerateCSR}>Generate</button>
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