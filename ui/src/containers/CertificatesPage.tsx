import * as React from 'react';
import {connect, Dispatch} from 'react-redux';
import Griddle, {RowDefinition, ColumnDefinition} from 'griddle-react';

import {IndexActionRequest} from "../actions/certificates";
import {bindActionCreators} from "redux";
import * as apiActions from '../actions/certificates';
import {CertificatesState} from "../reducers/certificates";
import {RootState} from "../reducers/index";
import {RouteComponentProps} from "react-router";

interface ReduxStateProps {
    certificates: CertificatesState;
}

interface ReduxDispatchProps {
    index: IndexActionRequest;
}

interface CertificatesPageProps extends ReduxStateProps, ReduxDispatchProps, RouteComponentProps<any> {
}

interface CertificatesPageState {
    filter: string;
}

@connect<ReduxStateProps, ReduxDispatchProps, CertificatesPageProps>(
    (state: RootState, ownProps?: any): ReduxStateProps => {
        return { certificates: state.certificates };
    },
    (dispatch: Dispatch<any>): ReduxDispatchProps => {
        return bindActionCreators({
            index: apiActions.index
        }, dispatch);
    }
)
export class CertificatesPage extends React.Component<CertificatesPageProps, CertificatesPageState> {

    componentWillMount(): void {
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
                                <ColumnDefinition title="Type" id="attributes.purpose" />
                                <ColumnDefinition title="Subject" id="attributes.subject" />
                            </RowDefinition>
                        </Griddle>
                    </div>
                </div>
            </div>
        );
    }
}