import * as React from "react";

import {
    Button,
    Header,
    Icon,
    Segment,
} from "semantic-ui-react";

import {format} from "date-fns";
import {VPPAccount} from "../../store/configuration/types";

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
