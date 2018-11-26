import Griddle, {ColumnDefinition, RowDefinition} from "griddle-react";
import * as React from "react";
import {connect, Dispatch} from "react-redux";
import {RouteComponentProps} from "react-router";
import {bindActionCreators} from "redux";
import {certificates as fetchInstalledCertificates, CertificatesActionRequest} from "../../store/device/certificates";
import {CertificateTypeIcon} from "../../components/CertificateTypeIcon";
import {CertificateRow} from "../../components/griddle/CertificateRow";
import {ListTableBody, ListTableContainer} from "../../components/griddle/ListTable";
import {SimpleLayout as Layout} from "../../components/griddle/SimpleLayout";
import {SemanticUIPlugin} from "../../griddle-plugins/semantic-ui/index";
import {griddle, GriddleDecoratorState} from "../../hoc/griddle";
import {InstalledCertificatesState} from "../../reducers/device/installed_certificates";
import {RootState} from "../../reducers/index";

interface ReduxStateProps {
    installed_certificates: InstalledCertificatesState;
}

function mapStateToProps(state: RootState, ownProps?: any): ReduxStateProps {
    return {
        installed_certificates: state.device.installed_certificates,
    };
}

interface ReduxDispatchProps {
    fetchInstalledCertificates: CertificatesActionRequest;
}

function mapDispatchToProps(dispatch: Dispatch<any>): ReduxDispatchProps {
    return bindActionCreators({
        fetchInstalledCertificates,
    }, dispatch);
}

interface DeviceCertificatesRouteProps {
    id: string; // device id
}

interface DeviceCertificatesProps extends ReduxStateProps, ReduxDispatchProps, RouteComponentProps<DeviceCertificatesRouteProps> {
    griddleState: GriddleDecoratorState;
    events: any;
}

interface DeviceCertificatesState {
}

export class UnconnectedDeviceCertificates extends React.Component<DeviceCertificatesProps, any> {

    public componentWillMount?() {
        this.props.fetchInstalledCertificates(this.props.match.params.id, this.props.griddleState.pageSize);
    }

    public componentWillUpdate(nextProps: DeviceCertificatesProps, nextState: DeviceCertificatesState) {
        const {griddleState} = this.props;
        const {griddleState: nextGriddleState} = nextProps;

        if (nextGriddleState.filter !== griddleState.filter || nextGriddleState.currentPage !== griddleState.currentPage) {
            this.props.fetchInstalledCertificates(
                "" + this.props.match.params.id,
                nextGriddleState.pageSize,
                nextGriddleState.currentPage, [],
                [{ name: "x509_cn", op: "ilike", val: `%${nextGriddleState.filter}%` }]);
        }
    }

    public render(): JSX.Element {
        const {
            installed_certificates,
            griddleState,
        } = this.props;

        return (
            <div className="DeviceCertificates">
                {installed_certificates.items &&
                <Griddle
                    data={installed_certificates.items}
                    plugins={[SemanticUIPlugin()]}
                    styleConfig={{
                        classNames: {
                            Table: "ui celled table",
                            NoResults: "ui message",
                        },
                    }}
                    events={this.props.events}
                    components={{
                        Layout,
                        Row: CertificateRow,
                        TableContainer: ListTableContainer,
                        TableBody: ListTableBody,
                    }}
                    pageProperties={{
                        currentPage: griddleState.currentPage,
                        pageSize: griddleState.pageSize,
                        recordCount: installed_certificates.recordCount,
                    }}
                >
                    <RowDefinition onClickButton={(e: any) => { console.log("clicked button"); }}>
                    </RowDefinition>
                </Griddle>}
            </div>
        );
    }
}

export const DeviceCertificates = connect<ReduxStateProps, ReduxDispatchProps, DeviceCertificatesProps>(
    mapStateToProps,
    mapDispatchToProps,
)(griddle(UnconnectedDeviceCertificates));
