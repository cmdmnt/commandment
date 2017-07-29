import * as React from 'react';
import {connect, Dispatch, MapStateToProps} from 'react-redux';
import {Container, Header, Item, Icon} from 'semantic-ui-react';
import {Link} from 'react-router-dom';
import {RouteComponentProps} from "react-router";
import {RootState} from "../../reducers/index";
import {bindActionCreators} from "redux";
import {read as fetchTokenInfo, TokenActionRequest} from "../../actions/vpp";
import {VPPState} from "../../reducers/configuration/vpp";


interface RouteProps {

}

interface ReduxStateProps {
    vpp: VPPState;
}

interface ReduxDispatchProps {
    fetchTokenInfo: TokenActionRequest;
}

interface OwnProps extends ReduxStateProps, ReduxDispatchProps, RouteComponentProps<RouteProps> {

}

export class UnconnectedVPPPage extends React.Component<OwnProps, void> {

    componentWillMount?() {
        this.props.fetchTokenInfo();
    }

    handleSubmit = (e: any) => {
        e.preventDefault();
        console.log('vpp submit');
    };

    render() {
        const {
            vpp
        } = this.props;

        return (
            <Container className='VPPPage'>
                <Header as='h1'>Volume Purchase Programme Configuration</Header>
                <p>
                    Upload a VPP Token
                </p>
                <form method='POST' action='/api/v1/vpp/upload/token' encType='multipart/form-data'>
                    <input type='file' name='file' />
                    <input type='submit' />
                </form>

                <Item>
                    <Item.Content>
                        <Item.Header>
                            <Icon name='ticket' />
                            VPP Token
                        </Item.Header>
                        <Item.Description>
                            Org {vpp.data && vpp.data.org_name}
                            Expires {vpp.data && vpp.data.exp_date}
                        </Item.Description>
                    </Item.Content>
                </Item>
            </Container>
        )
    }
}

export const VPPPage = connect<ReduxStateProps, ReduxDispatchProps, OwnProps>(
    (state: RootState): ReduxStateProps => ({
        vpp: state.configuration.vpp
    }),
    (dispatch: Dispatch<any>) => bindActionCreators({
        fetchTokenInfo
    }, dispatch)
)(UnconnectedVPPPage);
