import {SUIFilter as Filter} from "./components/SUIFilter";
import {SUIPagination as Pagination} from './components/SUIPagination';
import {SUIPageList as PageDropdown} from './components/SUIPageList';
import {SUINextButton as NextButton} from './components/SUINextButton';
import {SUIPrevButton as PrevButton} from './components/SUIPrevButton';
import {SUISettingsToggle as SettingsToggle} from './components/SUISettingsToggle';


export const SemanticUIPlugin = (config: any) => {
    return {
        components: {
            Filter,
            NextButton,
            PrevButton,
            PageDropdown,
            Pagination,
            SettingsToggle
        }
    }
};
