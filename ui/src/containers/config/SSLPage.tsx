import * as React from 'react';
import { connect, Dispatch } from 'react-redux';
import {RouteComponentProps} from 'react-router';
import { SCEPConfigurationForm, FormData } from '../../forms/SCEPConfigurationForm';


interface SSLPageState {

}

interface SSLPageDispatchProps {

}

interface SSLPageProps {

}

@connect()
export class SSLPage extends React.Component<SSLPageProps & RouteComponentProps<any>, SSLPageState> {

    handleSubmit = (values: FormData) => {

    };

    render() {
        const {
            children
        } = this.props;

        return (
            <div className='SSLPage container top-margin'>
                <div className='row'>
                    <div className='column'>
                        <h1>SSL Configuration</h1>

                        
                    </div>
                </div>
            </div>
        )
    }

}