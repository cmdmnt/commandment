import { action } from "@storybook/addon-actions";
import { storiesOf } from "@storybook/react";
import * as React from "react";
import Container from "semantic-ui-react/src/elements/Container";
import {WIFIPayloadForm} from "../WIFIPayloadForm";

storiesOf("WIFIPayloadForm", module)
    .add("default", () => (
        <Container>
            <WIFIPayloadForm onSubmit={action("submit")} />
        </Container>
    )).add("loading", () => (
    <Container>
        <WIFIPayloadForm onSubmit={action("submit")} loading />
    </Container>
    ));
