import * as React from 'react';
import { storiesOf } from '@storybook/react';
import { action } from '@storybook/addon-actions';
import {SCEPPayloadForm} from '../forms/payloads/SCEPPayloadForm';

storiesOf('SCEPPayloadForm', module)
    .add('default', () => {
        <SCEPPayloadForm onClickTest={action('test')} loading={false} submitted={false} />
    });