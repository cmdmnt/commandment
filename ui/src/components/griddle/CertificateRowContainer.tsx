import * as React from 'react';
import * as PropTypes from 'prop-types';
import { connect } from 'react-redux';
import {compose, mapProps, getContext} from 'recompose';
import {components, selectors, utils} from 'griddle-react';

const {
    columnIdsSelector,
    rowDataSelector,
    rowPropertiesSelector,
    classNamesForComponentSelector,
    stylesForComponentSelector
} = selectors;

const valueOrResult = utils.dataUtils.valueOrResult;

export interface CertificateRowContainerContext {
    components: any;
}

export interface CertificateRowContainerProps {
    columnIds?: number[];
    rowProperties?: any; // RowRenderProperties;
    rowData?: any;
    className?: string;
    style?: React.CSSProperties;
}

const ComposedRowContainer = (OriginalComponent: React.ComponentClass<components.RowProps>) => compose(
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
    mapProps((props: CertificateRowContainerProps & CertificateRowContainerContext) => {
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
