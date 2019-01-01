import * as React from "react";
import {connect, Dispatch} from "react-redux";
import {RouteComponentProps} from "react-router";
import {bindActionCreators} from "redux";
import {certificates as fetchInstalledCertificates, CertificatesActionRequest} from "../../store/device/certificates";
import {InstalledCertificatesState} from "../../reducers/device/installed_certificates";
import {RootState} from "../../reducers/index";
import {DeviceCertificatesTable} from "../../components/react-tables/DeviceCertificatesTable";
import {IReactTableState} from "../../store/table/types";
import {FlaskFilter, FlaskFilterOperation} from "../../store/constants";

interface IReduxStateProps {
    installed_certificates: InstalledCertificatesState;
}

function mapStateToProps(state: RootState, ownProps?: any): IReduxStateProps {
    return {
        installed_certificates: state.device.installed_certificates,
    };
}

interface IReduxDispatchProps {
    fetchInstalledCertificates: CertificatesActionRequest;
}

function mapDispatchToProps(dispatch: Dispatch<any>): IReduxDispatchProps {
    return bindActionCreators({
        fetchInstalledCertificates,
    }, dispatch);
}

interface IDeviceCertificatesRouteProps {
    id: string; // device id
}

type DeviceCertificatesProps = IReduxStateProps &
    IReduxDispatchProps &
    RouteComponentProps<IDeviceCertificatesRouteProps>;

export class UnconnectedDeviceCertificates extends React.Component<DeviceCertificatesProps, any> {
    public render(): JSX.Element {
        const {
            installed_certificates,
        } = this.props;

        return (
            <div className="DeviceCertificates">
                {installed_certificates.items &&
                <DeviceCertificatesTable
                    data={installed_certificates.items}
                    defaultPageSize={installed_certificates.pageSize}
                    loading={installed_certificates.loading}
                    onFetchData={this.fetchData}
                    pages={installed_certificates.pages}
                />}
            </div>
        );
    }

    private fetchData = (state: IReactTableState) => {
        const sorting = state.sorted.map((value) => (value.desc ? value.id : "-" + value.id));
        const filtering: FlaskFilter[] = state.filtered.map((value) => {
            return {
                name: value.id,
                op: "ilike" as FlaskFilterOperation,
                val: `%25${value.value}%25`,
            };
        });

        this.props.fetchInstalledCertificates(this.props.match.params.id, state.pageSize, state.page + 1, sorting, filtering);
    }
}

export const DeviceCertificates = connect<IReduxStateProps, IReduxDispatchProps, DeviceCertificatesProps>(
    mapStateToProps,
    mapDispatchToProps,
)(UnconnectedDeviceCertificates);
