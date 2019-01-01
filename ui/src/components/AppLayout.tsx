import * as React from "react";
import {hot} from "react-hot-loader";

import {Navigation} from "./Navigation";
import {NavigationVertical} from "./NavigationVertical";
import Sidebar from "semantic-ui-react/dist/commonjs/modules/Sidebar/Sidebar";
import Grid from "semantic-ui-react/dist/commonjs/collections/Grid/Grid";

/**
 * AppLayout is the top level root display component.
 *
 * It is recommended to keep this as a class and not a stateless component, due to earlier issues with react-router not
 * updating children.
 *
 * It is also recommended to keep this as an unconnected component for the same reason.
 *
 * @see https://github.com/ReactTraining/react-router/issues/4975
 */
class AppLayoutCool extends React.Component<{}, {}> {
    public render() {
        const {children} = this.props;

        return (
          <Grid>
              <Grid.Column width={4}>
                <NavigationVertical/>
              </Grid.Column>
              <Grid.Column width={12}>
                {children}
              </Grid.Column>
          </Grid>
        );
    }
}

export const AppLayout = hot(module)(AppLayoutCool);
