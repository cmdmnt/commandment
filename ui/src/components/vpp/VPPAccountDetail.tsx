import * as React from 'react';
import {Button, Item, Icon, Segment} from 'semantic-ui-react';
import {VPPAccount} from "../../models";
import * as moment from "moment";

export interface VPPAccountDetailProps extends VPPAccount {
}

export const VPPAccountDetail: React.StatelessComponent<VPPAccountDetailProps> = (props: VPPAccountDetailProps) => (
    <Segment>
        <Item.Group>
            <Item>
                <Item.Content>
                    <Item.Header>
                        <Icon name='ticket'/>
                        VPP Token ({props.org_name})
                    </Item.Header>
                    <Item.Meta>
                        Expires {moment(props.exp_date).format()}
                    </Item.Meta>
                    <Item.Description>
                        <Button icon="download" content=".vpptoken" />
                    </Item.Description>
                </Item.Content>
            </Item>
        </Item.Group>
    </Segment>
);