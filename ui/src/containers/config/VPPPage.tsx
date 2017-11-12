import * as React from 'react';
import {connect, Dispatch, MapStateToProps} from 'react-redux';
import {Container, Header, Item, Icon, Segment} from 'semantic-ui-react';
import {RouteComponentProps} from "react-router";
import {IRootState} from "../../reducers/index";
import {bindActionCreators} from "redux";
import {read as fetchTokenInfo, TokenActionRequest,
    upload, UploadActionRequest} from "../../actions/vpp";
import {VPPState} from "../../reducers/configuration/vpp";
import {VPPAccountDetail} from "../../components/vpp/VPPAccountDetail";
import * as Dropzone from "react-dropzone";


interface RouteProps {

}

interface ReduxStateProps {
    vpp: VPPState;
}

interface ReduxDispatchProps {
    fetchTokenInfo: TokenActionRequest;
    upload: UploadActionRequest;
}

interface OwnProps extends ReduxStateProps, ReduxDispatchProps, RouteComponentProps<RouteProps> {

}

export class UnconnectedVPPPage extends React.Component<OwnProps, void> {

    componentWillMount?() {
        this.props.fetchTokenInfo();
    }

    handleDrop = (files: Array<File>) => {
        this.props.upload(files[0]);
    };

    render() {
        const {
            vpp: {data, loading}
        } = this.props;

        return (
            <Container className='VPPPage'>
                <Header as='h1'>Volume Purchase Programme Configuration</Header>
                <Dropzone
                    onDrop={this.handleDrop}
                    className="dropzone"
                    activeClassName="dropzone-active"
                    rejectClassName="dropzone-reject"
                    style={{}}>
                    <Header as="h3">Drop .vpptoken or Click to upload</Header>
                </Dropzone>
                {data && <VPPAccountDetail {...data} />}
            </Container>
        )
    }
}

export const VPPPage = connect<ReduxStateProps, ReduxDispatchProps, OwnProps>(
    (state: IRootState): ReduxStateProps => ({
        vpp: state.configuration.vpp
    }),
    (dispatch: Dispatch<any>) => bindActionCreators({
        fetchTokenInfo,
        upload
    }, dispatch)
)(UnconnectedVPPPage);
