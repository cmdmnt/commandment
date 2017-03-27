import * as React from 'react';
import {ApUpload, ApUploadStyle} from 'apeman-react-upload';

interface APNSConfigurationProps {

}

export class APNSConfiguration extends React.Component<APNSConfigurationProps,undefined> {

    handleLoaded = (urls: Array<string>) => {
        console.dir(urls);
    };

    handleError = (err: Error) => {
        console.log(err);
    };

    render() {
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


                            <h3>Upload a Push Certificate</h3>
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