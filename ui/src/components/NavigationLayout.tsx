import * as React from "react";

import Grid from "semantic-ui-react/dist/commonjs/collections/Grid/Grid";
import {NavigationVertical} from "./NavigationVertical";
import {RouteComponentProps} from "react-router";
import {ComponentProps, FunctionComponent} from "react";

export const NavigationLayout: FunctionComponent<RouteComponentProps> = (props: RouteComponentProps & ComponentProps) => (
    <Grid className="NavigationLayout">
        <Grid.Column width={2}>
            <NavigationVertical/>
        </Grid.Column>
        <Grid.Column width={12}>
            {props.children}
        </Grid.Column>
    </Grid>
);
