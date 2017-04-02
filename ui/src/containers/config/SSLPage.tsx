import * as React from 'react';
import { connect, Dispatch } from 'react-redux';
import {RouteComponentProps} from 'react-router';
import {
    IndexActionRequest, index,
    DeleteCertificateActionRequest, remove
} from "../../actions/certificates";
import * as pushActions from '../../actions/certificates/push';
import * as sslActions from '../../actions/certificates/ssl';
import {bindActionCreators} from "redux";
import {CertificateDetail} from '../../components/CertificateDetail';
import * as Upload from 'rc-upload';
import {PushState} from "../../reducers/certificates/push";
import {SSLState} from "../../reducers/certificates/ssl";



interface SSLPageState {
    push: PushState;
    ssl: SSLState;
}

interface SSLPageDispatchProps {
    index: IndexActionRequest;
    remove: DeleteCertificateActionRequest;
    fetchPushCertificates: pushActions.FetchPushCertificatesActionRequest;
    fetchSSLCertificates: sslActions.FetchSSLCertificatesActionRequest;
}

interface SSLPageProps extends SSLPageState, SSLPageDispatchProps, RouteComponentProps<any> {

}

@connect<SSLPageState, SSLPageDispatchProps, SSLPageProps>(
    (state: any, ownProps?: any): SSLPageState => { return {
        push: state.certificates.push,
        ssl: state.certificates.ssl
    } },
    (dispatch: Dispatch<any>): SSLPageDispatchProps => {
        return bindActionCreators({
            index,
            fetchPushCertificates: pushActions.fetchPushCertificates,
            fetchSSLCertificates: sslActions.fetchSSLCertificates,
            remove
        }, dispatch);
    }
)
export class SSLPage extends React.Component<SSLPageProps, undefined> {

    componentWillMount() {
        this.props.fetchPushCertificates();
        this.props.fetchSSLCertificates();
    }

    handleDeleteCertificate = (certificateId: number): void => {
        this.props.remove(certificateId);
    };

    handleDownloadCertificate = (certificateId: number): void => {
        window.location.href = `/api/v1/certificates/${certificateId}/download`;
    };

    render(): JSX.Element {
        const {
            push,
            ssl
        } = this.props;

        let pushCertificate;
        if (push && push.items) {
            pushCertificate = push.items.data[0];
        }

        let sslCertificate;
        if (ssl && ssl.items) {
            sslCertificate = ssl.items.data[0];
        }

        return (
            <div className='SSLPage container top-margin'>
                <div className='row'>
                    <div className='column'>
                        <h1>SSL Configuration</h1>
                    </div>
                </div>
                <div className='row'>
                    <div className='column'>
                        <CertificateDetail certificate={pushCertificate} title="Push Certificate" onClickDelete={this.handleDeleteCertificate} onClickDownload={this.handleDownloadCertificate}>
                            <button className='button button-outline'>
                                <i className='fa fa-plus' /> Generate Request
                            </button>
                            <Upload
                                name='file'
                                accept='application/x-pem-file'
                                action='/api/v1/push/certificate/public'
                            >
                            <button className='button button-outline'>
                                <i className='fa fa-refresh' /> Replace
                            </button>
                            </Upload>

                        </CertificateDetail>
                    </div>
                    <div className='column'>
                        <CertificateDetail certificate={sslCertificate} title="SSL Certificate" onClickDelete={this.handleDeleteCertificate} onClickDownload={this.handleDownloadCertificate}>
                            <button className='button button-outline'>
                                <i className='fa fa-plus' /> Generate Request
                            </button>
                            <Upload
                                name='file'
                                accept='application/x-pem-file'
                                action='/api/v1/ssl_certificate_data'
                            >
                            <button className='button button-outline'>
                                <i className='fa fa-refresh' /> Replace
                            </button>
                            </Upload>
                            <button className='button button-outline'>
                                <i className='fa fa-download' /> Download
                            </button>
                        </CertificateDetail>
                    </div>
                    <div className='column'>
                        <CertificateDetail certificate={} title="SCEP CA Certificate" onClickDelete={this.handleDeleteCertificate} onClickDownload={this.handleDownloadCertificate}>
                            <Upload
                                name='file'
                                accept='application/x-pem-file'
                                action='/api/v1/scepca_certificate_data'
                            >
                                <button className='button button-outline'>
                                    <i className='fa fa-refresh' /> Replace
                                </button>
                            </Upload>
                            <button className='button button-outline'>
                                <i className='fa fa-download' /> Download
                            </button>
                        </CertificateDetail>
                    </div>
                </div>
            </div>
        )
    }

}