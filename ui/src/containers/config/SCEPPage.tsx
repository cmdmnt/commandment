import * as React from 'react';
import { connect, Dispatch } from 'react-redux';
import {RouteComponentProps} from 'react-router';
import { SCEPConfigurationForm, FormData } from '../../forms/SCEPConfigurationForm';


interface SCEPPageState {

}

interface SCEPPageDispatchProps {

}

interface SCEPPageProps {

}

@connect()
export class SCEPPage extends React.Component<SCEPPageProps & RouteComponentProps<any>, SCEPPageState> {

    handleSubmit = (values: FormData) => {
        
    };

    render() {
        const {
            children
        } = this.props;

        return (
            <div className='SCEPPage container top-margin'>
                <div className='row'>
                    <div className='column'>
                        <h1>SCEP Configuration</h1>
                        <SCEPConfigurationForm onSubmit={this.handleSubmit} />
                    </div>
                </div>
            </div>
        )
    }

}