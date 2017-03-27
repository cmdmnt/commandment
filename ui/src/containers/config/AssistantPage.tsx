import * as React from 'react';
import { connect, Dispatch } from 'react-redux';
import {RouteComponentProps} from 'react-router';
import {Assistant} from '../../components/Assistant';


interface AssistantPageState {

}

interface AssistantPageDispatchProps {

}

interface AssistantPageProps {

}

@connect(
    state => state.assistant
)
export class AssistantPage extends React.Component<AssistantPageProps & RouteComponentProps<any>, AssistantPageState> {

    handleSubmit = (values: FormData) => {
        
    };

    render() {
        const {
            children,
            currentStep,
            totalSteps
        } = this.props;

        return (
            <div className='AssistantPage container top-margin'>
                <Assistant currentStep={currentStep} totalSteps={totalSteps} components={[]} />
            </div>
        )
    }

}