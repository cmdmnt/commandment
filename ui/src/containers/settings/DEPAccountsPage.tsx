import * as React from "react";
import {connect, Dispatch, MapStateToProps} from "react-redux";
import Container from "semantic-ui-react/src/elements/Container";
import Header from "semantic-ui-react/src/elements/Header";

import * as Dropzone from "react-dropzone";
import {RouteComponentProps} from "react-router";
import {bindActionCreators} from "redux";
// import {read as fetchTokenInfo, TokenActionRequest,
//     upload, UploadActionRequest} from "../../actions/vpp";
import {VPPAccountDetail} from "../../components/vpp/VPPAccountDetail";
import {DEPState} from "../../reducers/configuration/dep";
import {RootState} from "../../reducers/index";

interface RouteProps {

}

interface ReduxStateProps {
    dep: DEPState;
}

interface ReduxDispatchProps {
    // fetchTokenInfo: TokenActionRequest;
    // upload: UploadActionRequest;
}

interface OwnProps extends ReduxStateProps, ReduxDispatchProps, RouteComponentProps<RouteProps> {

}

export class UnconnectedDEPAccountsPage extends React.Component<OwnProps, void> {

    componentWillMount?() {
        // this.props.fetchTokenInfo();
    }


    render() {
        const {
            dep: {data, loading},
        } = this.props;

        return (
            <Container className="VPPPage">
                <Header as="h1">DEP Accounts</Header>
                {/*<Dropzone*/}
                    {/*onDrop={this.handleDrop}*/}
                    {/*className="dropzone"*/}
                    {/*activeClassName="dropzone-active"*/}
                    {/*rejectClassName="dropzone-reject"*/}
                    {/*style={{}}>*/}
                    {/*<Header as="h3">Drop .vpptoken or Click to upload</Header>*/}
                {/*</Dropzone>*/}
                {data && <VPPAccountDetail {...data} />}
            </Container>
        );
    }
}

export const DEPAccountsPage = connect<ReduxStateProps, ReduxDispatchProps, OwnProps>(
    (state: RootState): ReduxStateProps => ({
        dep: state.configuration.dep,
    }),
    (dispatch: Dispatch<any>) => bindActionCreators({
        // fetchTokenInfo,
        // upload,
    }, dispatch),
)(UnconnectedDEPAccountsPage);
