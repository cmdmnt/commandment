import * as React from 'react';
import * as PropTypes from 'prop-types';
import { connect } from 'react-redux';
import {compose, mapProps, getContext} from 'recompose';
import {
    columnIdsSelector,
    rowDataSelector,
    rowPropertiesSelector,
    classNamesForComponentSelector,
    stylesForComponentSelector,
} from 'griddle-react/selectors/dataSelectors';
import { valueOrResult } from 'griddle-react/utils/valueUtils';

const ComposedRowContainer = (OriginalComponent: React.ComponentClass<any>) => compose(
    getContext({
        components: PropTypes.object,
    }),
    connect((state, props) => ({
        columnIds: columnIdsSelector(state),
        rowProperties: rowPropertiesSelector(state),
        rowData: rowDataSelector(state, props),
        className: classNamesForComponentSelector(state, 'Row'),
        style: stylesForComponentSelector(state, 'Row'),
    })),
    mapProps(props => {
        const { components, rowProperties, className, ...otherProps } = props;
        return {
            Cell: components.Cell,
            className: valueOrResult(rowProperties.cssClassName, props) || props.className,
            ...otherProps,
        };
    }),
)(props => (
    <OriginalComponent
        {...props}
    />
));

export default ComposedRowContainer;
