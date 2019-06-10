import * as React from "react";
import {connect, MapStateToProps} from "react-redux";
import {Dispatch} from "redux";
import {
    Container,
    Header,
} from "semantic-ui-react";

import {Component} from "react";
import * as Dropzone from "react-dropzone";
import {RouteComponentProps} from "react-router";
import {bindActionCreators} from "redux";
import {RootState} from "../../reducers/index";
import {index, IndexActionRequest,
    read as fetchTokenInfo, TokenActionRequest} from "../../store/configuration/vpp";
import {VPPState} from "../../store/configuration/vpp_reducer";

interface IReduxStateProps {
    vpp: VPPState;
}

interface IReduxDispatchProps {
    fetchTokenInfo: TokenActionRequest;
    index: IndexActionRequest;
}

export type UnconnectedVPPAccountsPageProps = IReduxStateProps & IReduxDispatchProps & RouteComponentProps<any>

export class UnconnectedVPPAccountsPage extends Component<UnconnectedVPPAccountsPageProps, any> {

    public componentWillMount?() {
        this.props.index();
    }

    // handleDrop = (files: File[]) => {
    //     this.props.upload(files[0]);
    // };

    public render() {
        const {
            vpp: {data, loading},
        } = this.props;

        return (
            <Container className="VPPAccountsPage">
                <Header as="h1">VPP Accounts</Header>
                {/*<Dropzone*/}
                    {/*onDrop={this.handleDrop}*/}
                    {/*className="dropzone"*/}
                    {/*activeClassName="dropzone-active"*/}
                    {/*rejectClassName="dropzone-reject"*/}
                    {/*style={{}}>*/}
                    {/*<Header as="h3">Drop .vpptoken or Click to upload</Header>*/}
                {/*</Dropzone>*/}
            </Container>
        );
    }
}

export const VPPAccountsPage = connect(
    (state: RootState): IReduxStateProps => ({
        vpp: state.configuration.vpp,
    }),
    (dispatch: Dispatch) => bindActionCreators({
        fetchTokenInfo,
        index,
    }, dispatch),
)(UnconnectedVPPAccountsPage);
