import * as React from 'react';
import {SCEPConfigurationForm} from '../SCEPConfigurationForm';

interface SCEPConfigurationProps {

}

export class SCEPConfiguration extends React.Component<SCEPConfigurationProps,undefined> {

    handleLoaded = (loaded: { urls: Array<string>, target: any }) => {
        console.dir(loaded.urls);
    };

    handleError = (err: Error) => {
        console.log(err);
    };


    render() {
        return (
            <div className='SCEPConfiguration'>
                <div className='reversed padded title'><i className="fa fa-mobile" /> SCEP Configuration</div>
                <div className='top-margin container'>
                    <div className='row'>
                        <div className='column'>
                            <p>Devices need to request identity certificates to prove that they are enrolled in your MDM.
                            This is done through a SCEP service. You can use the built-in service for testing, or
                            provide information about your production SCEP server.</p>
                        </div>
                    </div>
                    <div className='row'>
                        <div className='column'>
                            <SCEPConfigurationForm />
                        </div>
                    </div>
                </div>
            </div>
        )
    }
}