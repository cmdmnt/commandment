import * as React from 'react';
import {connect, Dispatch} from 'react-redux';
import Griddle, {RowDefinition, ColumnDefinition} from 'griddle-react';

import {IndexActionRequest} from "../actions/certificates";
import {bindActionCreators} from "redux";
import * as apiActions from '../actions/certificates';
import {CertificatesState} from "../reducers/certificates";
import {RootState} from "../reducers/index";
import {RouteComponentProps} from "react-router";
import * as webpack from "webpack";
import Filter = webpack.BannerPlugin.Filter;

interface OwnProps {

}

interface ReduxStateProps {
    certificates: CertificatesState;
}

function mapStateToProps(state: RootState, ownProps: OwnProps): ReduxStateProps {
    return { certificates: state.certificates };
}

interface ReduxDispatchProps {
    index: IndexActionRequest;
}

function mapDispatchToProps(dispatch: Dispatch<RootState>, ownProps: OwnProps): ReduxDispatchProps {
    return bindActionCreators({
        index: apiActions.index
    }, dispatch);
}

interface CertificatesPageProps extends ReduxStateProps, ReduxDispatchProps, RouteComponentProps<any> {
    handleFilter: (filterText: string) => void;
}

interface CertificatesPageState {
    filter: string;

}

class BaseCertificatesPage extends React.Component<CertificatesPageProps, CertificatesPageState> {

    componentWillMount?(): void {
        this.props.index();
    }

    handleFilter = (filterText: string) => {
        // TODO: debounce filter text
    };

    render(): JSX.Element {
        const {
            certificates
        } = this.props;

        const eventHandlers = {
            onFilter: this.handleFilter,
        };

        return (
            <div className='CertificatesPage top-margin container'>
                <div className='row'>
                    <div className='column'>
                        <h1>Certificates</h1>
                    </div>
                </div>
                <div className='row'>
                    <div className='column'>
                        <Griddle
                            data={certificates.items}
                            pageProperties={{
                                currentPage: certificates.currentPage,
                                pageSize: certificates.pageSize,
                                recordCount: certificates.recordCount
                            }}
                            events={eventHandlers}
                        >
                            <RowDefinition>
                                <ColumnDefinition id="id" />
                                <ColumnDefinition title="Type" id="attributes.type" />
                                <ColumnDefinition title="Common Name" id="attributes.x509_cn" />
                            </RowDefinition>
                        </Griddle>
                    </div>
                </div>
            </div>
        );
    }
}

export const CertificatesPage = connect<ReduxStateProps, ReduxDispatchProps, CertificatesPageProps>(
    mapStateToProps,
    mapDispatchToProps
)(BaseCertificatesPage);