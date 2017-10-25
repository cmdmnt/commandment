import * as React from 'react';
import { storiesOf } from '@storybook/react';
import { action } from '@storybook/addon-actions';
import {Container} from 'semantic-ui-react';
import {WIFIPayloadForm} from '../WIFIPayloadForm';

storiesOf('WIFIPayloadForm', module)
    .add('default', () => (
        <Container>
            <WIFIPayloadForm onSubmit={action('submit')} />
        </Container>
    )).add('loading', () => (
    <Container>
        <WIFIPayloadForm onSubmit={action('submit')} loading />
    </Container>
    ));