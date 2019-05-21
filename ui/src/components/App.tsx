import * as React from "react";
import {hot} from "react-hot-loader";

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
class AppCool extends React.Component<{}, {}> {
    public render() {
        const {children} = this.props;

        return (
          <div className="App">
              {children}
          </div>
        );
    }
}

export const App = hot(module)(AppCool);
