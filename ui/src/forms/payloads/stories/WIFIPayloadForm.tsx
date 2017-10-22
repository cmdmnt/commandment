import * as React from 'react';
import {storiesOf} from '@storybook/react';
import {WIFIPayloadForm} from '../WIFIPayloadForm';

storiesOf('WIFIPayloadForm', module)
    .add('default', () => (
        <WIFIPayloadForm />
    ));