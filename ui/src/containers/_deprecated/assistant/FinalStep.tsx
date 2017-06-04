import * as React from 'react';

interface FinalStepProps {

}

export class FinalStep extends React.Component<FinalStepProps,undefined> {

    render() {
        return (
            <div className='FinalStep'>
                <div className='reversed padded title'><i className="fa fa-thumbs-up" /> Success</div>
                <div className='top-margin container centered'>
                    <div className='row'>
                        <div className='column'>
                            <p>Congratulations, your commandment server is set up!</p>

                            <p>If your devices are not DEP provisioned,
                            use the link below to download an enrollment profile.</p>

                            <button className='button'>Enroll</button>
                        </div>
                    </div>
                </div>
            </div>
        )
    }
}