import { configure } from '@storybook/react';

function loadStories() {
  require('../src/stories/index.ts');
}

configure(loadStories, module);
