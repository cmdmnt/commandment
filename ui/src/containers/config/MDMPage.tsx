import * as React from 'react';
import { connect, Dispatch } from 'react-redux';
import {RouteComponentProps} from 'react-router';
import { MDMConfigurationForm, FormData } from '../../forms/MDMConfigurationForm';
import {FetchCertificateTypeActionRequest, fetchCertificatesForType} from "../../actions/certificates";
import {bindActionCreators} from "redux";


interface MDMPageState {
    byType?: {[propName: string]: JSONAPIDetailResponse<Certificate>};
}

interface MDMPageDispatchProps {
    fetchCertificatesForType: FetchCertificateTypeActionRequest;
}

interface MDMPageProps extends MDMPageState, MDMPageDispatchProps, RouteComponentProps<any> {
    
}

@connect<MDMPageState, MDMPageDispatchProps, MDMPageProps>(
    (state: any, ownProps?: any): MDMPageState => { return {
        byType: state.certificates.byType || null
    } },
    (dispatch: Dispatch<any>): MDMPageDispatchProps => {
        return bindActionCreators({
            fetchCertificatesForType
        }, dispatch);
    }
)
export class MDMPage extends React.Component<MDMPageProps & RouteComponentProps<any>, MDMPageState> {

    componentWillMount(): void {
        this.props.fetchCertificatesForType('mdm.pushcert');
        this.props.fetchCertificatesForType('mdm.cacrt');
    }

    handleSubmit = (values: FormData) => {

    };

    render() {
        const {
            byType
        } = this.props;

        const pushCertificate = byType['mdm.pushcert'];
        const CACertificate = byType['mdm.cacrt'];

        return (
            <div className='MDMPage container top-margin'>
                <div className='row'>
                    <div className='column'>
                        <h1>MDM Configuration</h1>
                        <MDMConfigurationForm
                            onSubmit={this.handleSubmit}
                            PushCertificate={pushCertificate}
                            CACertificate={CACertificate}
                        />
                    </div>
                </div>
            </div>
        )
    }

}