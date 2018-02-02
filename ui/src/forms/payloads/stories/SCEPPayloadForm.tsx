import * as React from 'react';
import { storiesOf } from '@storybook/react';
import { action } from '@storybook/addon-actions';
import Container from "semantic-ui-react/src/elements/Container";
import {SCEPPayloadForm} from '../SCEPPayloadForm';

storiesOf('SCEPPayloadForm', module)
    .add('default', () => (
        <Container>
            <SCEPPayloadForm onSubmit={action('submit')} loading={false} submitted={false} />
        </Container>
    )).add('loading', () => (
        <Container>
            <SCEPPayloadForm onSubmit={action('submit')} loading={true} submitted={false} />
        </Container>
    ));
