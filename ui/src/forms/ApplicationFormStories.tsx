import * as React from 'react';
import {storiesOf, action} from '@kadira/storybook';
import {Container} from 'semantic-ui-react';
import {ApplicationForm} from './ApplicationForm';

storiesOf('ApplicationForm', module)
    .add('default', () => (
        <Container>
            <ApplicationForm onSubmit={action('onSubmit')}/>
        </Container>
    ));
