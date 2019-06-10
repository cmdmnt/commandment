import { action } from "@storybook/addon-actions";
import { storiesOf } from "@storybook/react";
import * as React from "react";
import {Container} from "semantic-ui-react";
import {DEPProfileForm} from "../components/forms/DEPProfileForm";

storiesOf("DEPProfileForm", module)
    .add("default", () => (
        <Container>
            <DEPProfileForm
                loading={false}
                onSubmit={action("onSubmit")}
                activeIndex={1}
                onClickAccordionTitle={action("onClickTitle")}
            />
        </Container>
    ));
