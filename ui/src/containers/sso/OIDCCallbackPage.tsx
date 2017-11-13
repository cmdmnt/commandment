import * as React from "react";
import {connect, Dispatch} from "react-redux";
import {CallbackComponent} from "redux-oidc";
import {userManager} from "../../reducers/oidc";
import {IRootState} from "../../reducers/index";

class UnconnectedOIDCCallbackPage extends React.Component {

    successCallback = (user: Oidc.User) => {
      console.dir(user);
    };

    render() {
        return <CallbackComponent userManager={userManager} successCallback={this.successCallback}/>
    }
}

export const OIDCCallbackPage = connect(
    null,
    (dispatch: Dispatch<IRootState>) => ({ dispatch })
)(UnconnectedOIDCCallbackPage);
