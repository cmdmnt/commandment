import * as React from 'react';
import {connect, Dispatch} from 'react-redux';
import {RouteComponentProps} from 'react-router';
import {RootState} from "../../reducers/index";
import {bindActionCreators} from "redux";
import {CertificatesActionRequest, certificates as fetchInstalledCertificates} from "../../actions/devices";
import {installed_certificates, InstalledCertificatesState} from "../../reducers/device/installed_certificates";
import Griddle, {RowDefinition, ColumnDefinition, SortProperties} from 'griddle-react';
import {SemanticUIPlugin} from "../../griddle-plugins/semantic-ui/index";
import {SimpleLayout as Layout} from "../../components/griddle/SimpleLayout";
import {CertificateTypeIcon} from "../../components/CertificateTypeIcon";

interface ReduxStateProps {
    installed_certificates: InstalledCertificatesState;
}

function mapStateToProps(state: RootState, ownProps?: any): ReduxStateProps {
    return {
        installed_certificates: state.device.installed_certificates
    }
}

interface ReduxDispatchProps {

}

function mapDispatchToProps(dispatch: Dispatch<any>): ReduxDispatchProps {
    return bindActionCreators({
        fetchInstalledCertificates
    }, dispatch);
}

interface RouterProps {
    id: string; // device id
}

interface DeviceCertificatesProps extends ReduxStateProps, ReduxDispatchProps, RouteComponentProps<RouterProps> {

}

@connect<ReduxStateProps, ReduxDispatchProps, DeviceCertificatesProps>(
    mapStateToProps,
    mapDispatchToProps
)
export class DeviceCertificates extends React.Component<DeviceCertificatesProps, any> {

    componentWillMount() {
        this.props.fetchInstalledCertificates(this.props.match.params.id, 25);
    }

    onFilter = (value: string) => {
        console.log('filterr');
    };

    render(): JSX.Element {
        const {
            installed_certificates
        } = this.props;

        return (
            <div className='DeviceCertificates'>

                        {installed_certificates.items &&
                        <Griddle
                            data={installed_certificates.items}
                            plugins={[SemanticUIPlugin()]}
                            styleConfig={{
                                classNames: {
                                    Table: 'ui celled table'
                                }
                            }}
                            events={{
                                onFilter: this.onFilter
                                // onSort: this.onSort
                            }}
                            components={{
                                Layout
                            }}
                            pageProperties={installed_certificates.pageProperties}
                        >
                            <RowDefinition>
                                <ColumnDefinition id="id" />
                                <ColumnDefinition title='Identity' id="attributes.is_identity" customComponent={CertificateTypeIcon} />
                                <ColumnDefinition title='X.509 CN' id='attributes.x509_cn' />
                            </RowDefinition>
                        </Griddle>}
            </div>
        )
    }
}