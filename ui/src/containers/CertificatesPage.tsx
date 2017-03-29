import * as React from 'react';
import {connect, Dispatch} from 'react-redux';
import Griddle, {RowDefinition, ColumnDefinition} from 'griddle-react';

import {IndexActionRequest} from "../actions/certificates";
import {bindActionCreators} from "redux";
import * as apiActions from '../actions/certificates';
import {CertificatesState} from "../reducers/certificates";

interface StateProps {
    certificates: CertificatesState;
}

interface DispatchProps {
    index: IndexActionRequest;
}

interface CertificatesPageProps extends StateProps, DispatchProps {
}

@connect<StateProps, DispatchProps, CertificatesPageProps>(
    (state: any, ownProps?: any): StateProps => {
        return { certificates: state.certificates };
    },
    (dispatch: Dispatch<any>): DispatchProps => {
        return bindActionCreators({
            index: apiActions.index
        }, dispatch);
    }
)
export class CertificatesPage extends React.Component<CertificatesPageProps, any> {

    componentWillMount(): void {
        this.props.index();
    }

    render(): JSX.Element {
        const {
            certificates
        } = this.props;

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
                            events={{
                            }}
                        >
                            <RowDefinition>
                                <ColumnDefinition id="attributes.id" />
                                <ColumnDefinition id="cert_type" />
                            </RowDefinition>
                        </Griddle>
                    </div>
                </div>
            </div>
        );
    }
}