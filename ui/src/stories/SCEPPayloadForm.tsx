import * as React from 'react';
import {storiesOf, action} from '@kadira/storybook';
import {SCEPPayloadForm} from '../forms/payloads/SCEPPayloadForm';

storiesOf('SCEPPayloadForm', module)
    .add('default', () => {
        <SCEPPayloadForm/>
    });