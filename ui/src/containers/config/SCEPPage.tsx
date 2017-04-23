import * as React from 'react';
import {connect, Dispatch, MapStateToProps} from 'react-redux';
import {RouteComponentProps} from 'react-router';
import { SCEPConfigurationForm, FormData } from '../../forms/SCEPConfigurationForm';
import {SCEPPayloadForm} from '../../forms/payloads/SCEPPayloadForm';
import * as actions from '../../actions/configuration/scep';
import {RootState} from "../../reducers/index";
import {bindActionCreators} from "redux";
import {SCEPState} from "../../reducers/configuration/scep";


interface ReduxStateProps {
    scep: SCEPState;
}

function mapStateToProps(state: RootState): ReduxStateProps {
    return {
        scep: state.configuration.scep
    }
}

interface ReduxDispatchProps {
    read: actions.ReadActionRequest;
    post: actions.PostActionRequest;
}

function mapDispatchToProps(dispatch: Dispatch<any>) {
    return bindActionCreators({
        post: actions.post,
        read: actions.read
    }, dispatch);
}

interface OwnProps extends ReduxStateProps, ReduxDispatchProps, RouteComponentProps<{}> {

}

@connect<ReduxStateProps, ReduxDispatchProps, OwnProps>(
    mapStateToProps,
    mapDispatchToProps
)
export class SCEPPage extends React.Component<OwnProps, undefined> {

    componentWillMount() {
        this.props.read();
    }

    handleSubmit = (values: FormData): void => {
        this.props.post(values);
    };

    handleTest = () => {

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
                        <p>
                            The SCEP Configuration controls the parameters of certificates issued to devices via your
                            SCEP service.
                        </p>
                        <SCEPPayloadForm onSubmit={this.handleSubmit} onClickTest={this.handleTest} />
                    </div>
                </div>
            </div>
        )
    }

}