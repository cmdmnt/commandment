import * as React from 'react';
import {storiesOf, action} from '@kadira/storybook';
import {WIFIPayloadForm} from '../WIFIPayloadForm';

storiesOf('WIFIPayloadForm', module)
    .add('default', () => (
        <WIFIPayloadForm />
    ));