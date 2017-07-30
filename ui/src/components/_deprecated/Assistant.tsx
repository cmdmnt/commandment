import * as React from 'react';

import './Assistant.scss';

interface AssistantProps {
    totalSteps: number;
    currentStep: number;
    components: Array<React.ReactNode>;
    onClickNext: () => void;
    onClickPrev: () => void;
}

interface AssistantState {
    
}

export class Assistant extends React.Component<AssistantProps, AssistantState> {

    handleClickNext = (event: any): void => {
        event.preventDefault();
        this.props.onClickNext();
    };

    handleClickPrev = (event: any): void => {
        event.preventDefault();
        this.props.onClickPrev();
    };

    render(): JSX.Element {
        const {
            currentStep,
            totalSteps,
            components
        } = this.props;

        const dots = [];
        for (let x = 0; x < totalSteps; x++) {
            if (x == currentStep) {
                dots.push(<i key={x} className='fa fa-circle step-indicator step-indicator-active' />)
            } else {
                dots.push(<i key={x} className='fa fa-circle step-indicator'/>)
            }
        }

        return (
            <div className='Assistant paper'>
                <div className='steps'>
                    {components.map((component: any, idx: number) => {
                        if (currentStep === idx) {
                            return <div key={idx} className='step step-active'>{component}</div>;
                        } else {
                            return <div key={idx} className='step'>{component}</div>;
                        }
                    })}
                </div>
                <div className='buttons padded-sides clearfix row'>
                    <div className='column'>
                        { currentStep > 0 && <button className="button button-outline" onClick={this.handleClickPrev}>Previous</button> }
                    </div>
                    <div className='column'>
                        <span className='step-indicators'>{dots}</span>
                    </div>
                    <div className='column'>
                        { currentStep < totalSteps && <button className="button float-right" onClick={this.handleClickNext}>Next</button> }
                    </div>
                </div>
            </div>
        )
    }
}