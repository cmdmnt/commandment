import * as React from "react";

import {Navigation} from "./Navigation";

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
export class AppLayout extends React.Component<{}, void> {
    public render() {
        const {children} = this.props;

        return (
            <div>
                <Navigation/>
                {children}
            </div>
        );
    }
}
