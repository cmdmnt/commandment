import { configure } from '@kadira/storybook';

function loadStories() {
  require('../src/stories/index.ts');
}

configure(loadStories, module);
