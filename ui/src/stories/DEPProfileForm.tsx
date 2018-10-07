import * as React from 'react';
import { storiesOf } from '@storybook/react';
import { action } from '@storybook/addon-actions';
import Container from "semantic-ui-react/src/elements/Container";
import {DEPProfileForm} from "../components/forms/DEPProfileForm";

storiesOf('DEPProfileForm', module)
    .add('default', () => (
        <Container>
            <DEPProfileForm onSubmit={action('onSubmit')}/>
        </Container>
    ));
