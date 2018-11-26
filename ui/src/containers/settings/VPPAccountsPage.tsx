import * as React from "react";
import {connect, Dispatch, MapStateToProps} from "react-redux";
import Container from "semantic-ui-react/src/elements/Container";
import Header from "semantic-ui-react/src/elements/Header";

import * as Dropzone from "react-dropzone";
import {RouteComponentProps} from "react-router";
import {bindActionCreators} from "redux";
import {read as fetchTokenInfo, TokenActionRequest,
    index, IndexActionRequest} from "../../store/configuration/vpp";
import {VPPState} from "../../reducers/configuration/vpp";
import {RootState} from "../../reducers/index";

interface RouteProps {

}

interface ReduxStateProps {
    vpp: VPPState;
}

interface ReduxDispatchProps {
    fetchTokenInfo: TokenActionRequest;
    index: IndexActionRequest;
}

interface OwnProps extends ReduxStateProps, ReduxDispatchProps, RouteComponentProps<RouteProps> {

}

export class UnconnectedVPPAccountsPage extends React.Component<OwnProps, any> {

    componentWillMount?() {
        this.props.index();
    }

    // handleDrop = (files: File[]) => {
    //     this.props.upload(files[0]);
    // };

    render() {
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
    (state: RootState): ReduxStateProps => ({
        vpp: state.configuration.vpp,
    }),
    (dispatch: Dispatch<any>) => bindActionCreators({
        fetchTokenInfo,
        index,
    }, dispatch),
)(UnconnectedVPPAccountsPage);
