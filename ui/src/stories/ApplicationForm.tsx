import * as React from 'react';
import { storiesOf } from '@storybook/react';
import { action } from '@storybook/addon-actions';
import Container from "semantic-ui-react/src/elements/Container";
import {ApplicationForm} from '../forms/ApplicationForm';

storiesOf('ApplicationForm', module)
    .add('default', () => (
        <Container>
            <ApplicationForm onSubmit={action('onSubmit')}/>
        </Container>
    ));
