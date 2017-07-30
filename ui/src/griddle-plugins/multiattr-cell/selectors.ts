import {selectors} from 'griddle-react';
const cellPropertiesSelector = selectors.cellPropertiesSelector;

export const cellValueSelector = (state: any, props: any) => {
    console.log('cell value selector');
    const { griddleKey, columnId } = props;
    const cellProperties = cellPropertiesSelector(state, props);

    const lookup = state.getIn(['lookup', griddleKey.toString()]);
    const columnIds = columnId.split(',');

    const values = columnIds.map((cid: string) => {
        return state
            .get('data').get(lookup)
            .getIn(cid.split('.'));
    });

    return values;
};