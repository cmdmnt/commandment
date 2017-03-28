import * as React from 'react';
import { connect, Dispatch } from 'react-redux';
import {RouteComponentProps} from 'react-router';
import {IndexAction, index, FetchPushCertificateAction, fetchPushCertificate} from "../../actions/certificates";
import {bindActionCreators} from "redux";


interface SSLPageState {

}

interface SSLPageDispatchProps {
    index: IndexAction;
    fetchPushCertificate: FetchPushCertificateAction;
}

interface SSLPageProps {

}

@connect(
    (state: any, ownProps?: any) => { return {} },
    (dispatch: Dispatch<any>) => {
        return bindActionCreators({
            index,
            fetchPushCertificate
        }, dispatch);
    }
)
export class SSLPage extends React.Component<SSLPageProps & SSLPageState & SSLPageDispatchProps, SSLPageState> {

    componentWillMount() {
        this.props.fetchPushCertificate();
    }

    render(): JSX.Element {
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