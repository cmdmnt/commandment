import { configure } from '@storybook/react';

const req = require.context('../src/stories', true, /.stories.tsx$/);

function loadStories() {
  require('../src/stories/index.ts');
}

configure(loadStories, module);
