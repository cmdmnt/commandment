import * as React from "react";

import Button from "semantic-ui-react/src/elements/Button";
import Header from "semantic-ui-react/src/elements/Header";
import Icon from "semantic-ui-react/src/elements/Icon";
import Segment from "semantic-ui-react/src/elements/Segment";

import * as moment from "moment";
import {VPPAccount} from "../../models";

export interface IVPPAccountDetailProps extends VPPAccount {
}

export const VPPAccountDetail: React.StatelessComponent<IVPPAccountDetailProps> = (props: IVPPAccountDetailProps) => (
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
