import * as React from "react";

import Grid from "semantic-ui-react/dist/commonjs/collections/Grid/Grid";
import {NavigationVertical} from "./NavigationVertical";
import {Route, RouteProps} from "react-router";
import {ComponentClass, FunctionComponent} from "react";

interface INavigationLayout {
    component: ComponentClass;
}

export const NavigationLayout: FunctionComponent<INavigationLayout & RouteProps> = ({ Component: component, ...rest }) => (
    <Route {...rest} render={matchProps => (
        <Grid className="NavigationLayout">
            <Grid.Column width={4}>
                <NavigationVertical/>
            </Grid.Column>
            <Grid.Column width={12}>
                <Component {...matchProps} />
            </Grid.Column>
        </Grid>
    )} />
);
