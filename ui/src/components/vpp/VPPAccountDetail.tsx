import * as React from "react";

import Button from "semantic-ui-react/src/elements/Button";
import Header from "semantic-ui-react/src/elements/Header";
import Icon from "semantic-ui-react/src/elements/Icon";
import Segment from "semantic-ui-react/src/elements/Segment";

import {format} from "date-fns";
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
        Expires {format(props.exp_date)}
        <Button icon="download" content=".vpptoken" />

    </Segment>
);
