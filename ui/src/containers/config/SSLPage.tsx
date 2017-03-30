import * as React from 'react';
import { connect, Dispatch } from 'react-redux';
import {RouteComponentProps} from 'react-router';
import {
    IndexActionRequest, index,
    FetchCertificateTypeActionRequest, fetchCertificatesForType, DeleteCertificateActionRequest, remove
} from "../../actions/certificates";
import {bindActionCreators} from "redux";
import {CertificateDetail} from '../../components/CertificateDetail';
import * as Upload from 'rc-upload';


interface SSLPageState {
    byType?: {[propName: string]: JSONAPIDetailResponse<Certificate>};
}

interface SSLPageDispatchProps {
    index: IndexActionRequest;
    remove: DeleteCertificateActionRequest;
    fetchCertificatesForType: FetchCertificateTypeActionRequest;
}

interface SSLPageProps extends SSLPageState, SSLPageDispatchProps, RouteComponentProps<any> {

}

@connect<SSLPageState, SSLPageDispatchProps, SSLPageProps>(
    (state: any, ownProps?: any): SSLPageState => { return {
        byType: state.certificates.byType || null
    } },
    (dispatch: Dispatch<any>): SSLPageDispatchProps => {
        return bindActionCreators({
            index,
            fetchCertificatesForType,
            remove
        }, dispatch);
    }
)
export class SSLPage extends React.Component<SSLPageProps, undefined> {

    componentWillMount() {
        this.props.fetchCertificatesForType('mdm.pushcert');
        this.props.fetchCertificatesForType('mdm.webcrt');
        this.props.fetchCertificatesForType('mdm.cacrt');
    }

    handleDeleteCertificate = (certificateId: number): void => {
        this.props.remove(certificateId);
    };

    render(): JSX.Element {
        const {
            byType
        } = this.props;

        let pushCertificate;
        if (byType.hasOwnProperty('mdm.pushcert')) {
            pushCertificate = byType['mdm.pushcert'];
        }

        let sslCertificate;
        if (byType.hasOwnProperty('mdm.webcrt')) {
            sslCertificate = byType['mdm.webcrt'];
        }

        let scepCACertificate;
        if (byType.hasOwnProperty('mdm.cacrt')) {
            scepCACertificate = byType['mdm.cacrt'];
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
                        <CertificateDetail certificate={pushCertificate} title="Push Certificate" onClickDelete={this.handleDeleteCertificate}>
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
                            <button className='button button-outline'>
                                <i className='fa fa-download' /> Download
                            </button>
                        </CertificateDetail>
                    </div>
                    <div className='column'>
                        <CertificateDetail certificate={sslCertificate} title="SSL Certificate" onClickDelete={this.handleDeleteCertificate}>
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
                        <CertificateDetail certificate={scepCACertificate} title="SCEP CA Certificate" onClickDelete={this.handleDeleteCertificate}>
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