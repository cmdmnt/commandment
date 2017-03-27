import * as React from 'react';

interface AssistantProps {
    totalSteps: number;
    currentStep: number;
    components: Array<React.Component<any,any>>;
}

interface AssistantState {
    
}

export class Assistant extends React.Component<AssistantProps, AssistantState> {
    render() {
        const {
            currentStep,
            totalSteps,
            components
        } = this.props;

        const component = components[currentStep];

        return (
            <div className='Assistant'>
                <div className='content'>
                    {component}
                </div>
                <div className='pager'>
                    step {currentStep} of {totalSteps}
                </div>
                <div className='buttons'>
                    { currentStep > 0 && <button className="button button-outline">Previous</button> }
                    { currentStep < totalSteps && <button className="button">Next</button> }
                </div>
            </div>
        )
    }
}