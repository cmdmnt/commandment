import * as React from 'react';
import { connect, Dispatch } from 'react-redux';
import {RouteComponentProps} from 'react-router';
import {
    IndexActionRequest, index,
    DeleteCertificateActionRequest, remove
} from "../src/actions/certificates";
import * as caActions from '../src/actions/certificates/ca';
import {bindActionCreators} from "redux";
import {CertificateDetail} from '../src/components/_deprecated/CertificateDetail';
import {CAState} from "../src/reducers/certificates/ca";
import {CAConfigurationForm} from '../src/forms/_retired/CAConfigurationForm';

interface CAPageState {
    ca: CAState;
}

interface CAPageDispatchProps {
    remove: DeleteCertificateActionRequest;
    fetchCACertificates: caActions.FetchCACertificatesActionRequest;
}

interface CAPageProps extends CAPageState, CAPageDispatchProps, RouteComponentProps<any> {

}

@connect<CAPageState, CAPageDispatchProps, CAPageProps>(
    (state: any, ownProps?: any): CAPageState => { return {
        ca: state.certificates.ca
    } },
    (dispatch: Dispatch<any>): CAPageDispatchProps => {
        return bindActionCreators({
            fetchCACertificates: caActions.fetchCACertificates,
            remove
        }, dispatch);
    }
)
export class InternalCAPage extends React.Component<CAPageProps, undefined> {

    componentWillMount?() {
        this.props.fetchCACertificates();
    }

    handleDeleteCertificate = (certificateId: number): void => {
        this.props.remove(certificateId);
    };

    handleDownloadCertificate = (certificateId: number): void => {
        window.location.href = `/api/v1/certificates/${certificateId}/download`;
    };

    handleSubmit = (values: FormData): void => {

    };

    render(): JSX.Element {
        const {
            ca
        } = this.props;

        let caCertificate;
        if (ca && ca.items) {
            caCertificate = ca.items.data[0];
        }

        return (
            <div className='CAPage container top-margin'>
                <div className='row'>
                    <div className='column'>
                        <h1>Internal CA</h1>
                    </div>
                </div>
                <div className='row'>
                    <div className='column column-25'>
                        <CertificateDetail
                            certificate={caCertificate}
                            title="Certificate"
                            onClickDelete={this.handleDeleteCertificate}
                            onClickDownload={this.handleDownloadCertificate}
                        >
                        </CertificateDetail>
                    </div>
                    <div className='column'>
                        <CAConfigurationForm onSubmit={this.handleSubmit} />
                    </div>
                </div>
                <div className='row'>
                    <div className='column top-margin'>
                        <h2>Issued certificates</h2>
                    </div>
                </div>
            </div>
        )
    }

}