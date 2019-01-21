import {IDEPAccountsState} from "../../store/dep/accounts_reducer";
import {accounts, AccountIndexActionCreator} from "../../store/dep/actions";
import {RouteComponentProps} from "react-router";
import * as React from "react";
import Container from "semantic-ui-react/src/elements/Container/Container";
import Header from "semantic-ui-react/src/elements/Header/Header";

import {connect} from "react-redux";
import {RootState} from "../../reducers";
import {bindActionCreators, Dispatch} from "redux";
import Icon from "semantic-ui-react/dist/commonjs/elements/Icon/Icon";
import Button from "semantic-ui-react/dist/commonjs/elements/Button/Button";
import Step from "semantic-ui-react/dist/commonjs/elements/Step/Step";
import Grid from "semantic-ui-react/dist/commonjs/collections/Grid/Grid";
import Segment from "semantic-ui-react/dist/commonjs/elements/Segment/Segment";
import Divider from "semantic-ui-react/dist/commonjs/elements/Divider/Divider";

interface ReduxStateProps {
    accounts: IDEPAccountsState;
}

interface ReduxDispatchProps {
    getAccounts: AccountIndexActionCreator;
}

interface OwnProps extends ReduxStateProps, ReduxDispatchProps, RouteComponentProps<any> {

}

interface IDEPAccountSetupPageState {
    step: number;
}

export class UnconnectedDEPAccountSetupPage extends React.Component<OwnProps, IDEPAccountSetupPageState> {

    // static initialState: IDEPAccountPageState = {
    //     step: 0
    // };

    constructor(props: any) {
        super(props);
        this.state = { step: 0 };
    }

    public componentWillMount?() {
        //this.props.index();
    }

    public render() {
        const {
            accounts: {data, loading},
        } = this.props;

        return (
            <Container className="DEPAccountPage">
                <Header as="h1">Set up a New DEP Account</Header>
                <p>
                    Set up a New DEP Account to Sync Devices from Apple Business Manager or Apple School Manager to start
                    syncing your devices.
                </p>
                <Grid columns={2}>
                    <Grid.Column width={6}>
                        <Step.Group fluid vertical>
                            <Step active={this.state.step == 0} onClick={() => this.setState({ step: 0 })}>
                                <Icon name="download" />
                                <Step.Content>
                                    <Step.Title>Download</Step.Title>
                                    <Step.Description>Download a Public Key</Step.Description>
                                </Step.Content>
                            </Step>
                            <Step active={this.state.step == 1} onClick={() => this.setState({ step: 1 })}>
                                <Icon name="key" />
                                <Step.Content>
                                    <Step.Title>Upload Key</Step.Title>
                                    <Step.Description>Upload it to ABM/ASM to Get a Server Token</Step.Description>
                                </Step.Content>
                            </Step>
                            <Step active={this.state.step == 2} onClick={() => this.setState({ step: 2 })}>
                                <Icon name="upload" />
                                <Step.Content>
                                    <Step.Title>Upload Token</Step.Title>
                                    <Step.Description>Upload Server Token</Step.Description>
                                </Step.Content>
                            </Step>
                            <Step active={this.state.step == 3} onClick={() => this.setState({ step: 3 })}>
                                <Icon name="flag checkered" />
                                <Step.Content>
                                    <Step.Title>Sync Devices</Step.Title>
                                    <Step.Description>Start Syncing Devices</Step.Description>
                                </Step.Content>
                            </Step>
                        </Step.Group>
                    </Grid.Column>
                    <Grid.Column width={10}>
                        {this.state.step == 0 && <div>
                        <Button icon labelPosition='left' as={'a'} href="/dep/certificate/download" >
                            <Icon name='download' />
                            Download
                        </Button> a Public Key to use with Apple Business Manager or Apple School Manager
                        <Divider />
                        <p>
                            Before you can use the Public Key, you must create a new <em>MDM Server</em> in
                            Apple School Manager or Apple Business Manager.
                        </p>

                        <p>
                            Selecting the MDM Server you just created gives you the option to upload the Public Key
                            generated here.
                        </p>
                        </div>}

                        {this.state.step == 1 && <div>
                            <ul>
                                <li>Locate the Public Key <strong>(.cer file)</strong> downloaded in Step 1.</li>
                                <li>Log in to Apple School Manager or Apple Business Manager.</li>
                                <li>Create an MDM Server, or select one that you have already created.</li>
                                <li>Click the <Icon name="key" />Upload Key Button</li>
                            </ul>
                        </div>}

                    </Grid.Column>
                </Grid>
            </Container>
        );
    }
}

export const DEPAccountSetupPage = connect<ReduxStateProps, ReduxDispatchProps, OwnProps>(
    (state: RootState): ReduxStateProps => ({
        accounts: state.dep.accounts,
    }),
    (dispatch: Dispatch) => bindActionCreators({
        getAccounts: accounts,
    }, dispatch),
)(UnconnectedDEPAccountSetupPage);
