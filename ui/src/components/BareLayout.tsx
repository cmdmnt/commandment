import * as React from "react";

import {Grid} from "semantic-ui-react";
import {Route, RouteProps} from "react-router";
import {ComponentClass, FunctionComponent} from "react";

interface INavigationLayout {
    component: ComponentClass;
}

export const BareLayout: FunctionComponent<INavigationLayout & RouteProps> = ({ Component: component, ...rest }) => (
    <Route {...rest} render={matchProps => (
        <Grid className="BareLayout">
            <Component {...matchProps} />
        </Grid>
    )} />
);
