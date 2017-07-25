import {createSelector} from 'reselect';
import {SUIFilter as Filter} from "./components/SUIFilter";
import {SUIPagination as Pagination} from './components/SUIPagination';
import {SUIPageList as PageDropdown} from './components/SUIPageList';
import {SUINextButton as NextButton} from './components/SUINextButton';
import {SUIPrevButton as PreviousButton} from './components/SUIPrevButton';
import {SUISettingsToggle as SettingsToggle} from './components/SUISettingsToggle';

export interface SemanticUIPluginConfig {
    pagerIsDropdown?: boolean;
}

export interface SemanticUIPluginState {
    pluginConfig?: SemanticUIPluginConfig
}

export const SemanticUIPlugin = (pluginConfig?: SemanticUIPluginConfig) => {
    const initialState: SemanticUIPluginState = { pluginConfig };

    return {
        components: {
            Filter,
            NextButton,
            PreviousButton,
            PageDropdown,
            Pagination,
            SettingsToggle
        },
        initialState,
        selectors: {
            semanticUIPluginConfiguration: (state: any) => state.get('pluginConfig')
        }
    }
};
