import * as React from "react";
import Container from "semantic-ui-react/src/elements/Container/Container";
import {RouteComponentProps} from "react-router";

export const DashboardPage: React.FunctionComponent<RouteComponentProps<any>> = () => (
    <Container className="DashboardPage">
        <ul>
            <li><a href="/enroll/profile">Enroll (Direct)</a></li>
            <li><a href="/enroll/ota">Enroll (OTA)</a></li>
            <li><a href="/enroll/trust.mobileconfig">Download Trust Profile</a></li>
        </ul>
    </Container>
);
