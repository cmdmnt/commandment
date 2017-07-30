import * as React from 'react';
import {Button, Item, Icon, Segment, Header} from 'semantic-ui-react';
import {VPPAccount} from "../../models";
import * as moment from "moment";

export interface VPPAccountDetailProps extends VPPAccount {
}

export const VPPAccountDetail: React.StatelessComponent<VPPAccountDetailProps> = (props: VPPAccountDetailProps) => (
    <Segment>
        <Header as="h1">
            <Icon name="ticket" />
            <Header.Content>
                VPP Token ({props.org_name})
            </Header.Content>
        </Header>
        Expires {moment(props.exp_date).format()}
        <Button icon="download" content=".vpptoken" />

    </Segment>
);