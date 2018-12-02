import {components, connect, GriddleStyleConfig, selectors} from "griddle-react";
import {valueOrResult} from "griddle-react/dist/module/utils/valueUtils";
import * as React from "react";
import {CSSProperties} from "react";
import {MapDispatchToPropsFactory} from "react-redux";
import { compose, getContext, mapProps } from "recompose";
import {Store} from "redux";
import {toggleSelection as toggleSelectionAction} from "../actions";
import * as myselectors from "../selectors";

function hasWidthOrStyles(cellProperties: components.CellProps) {
    return cellProperties.hasOwnProperty("width") || cellProperties.hasOwnProperty("styles");
}

function getCellStyles(cellProperties: components.CellProps, originalStyles: CSSProperties) {
    if (!hasWidthOrStyles(cellProperties)) { return originalStyles; }

    let styles = originalStyles;

    // we want to take griddle style object styles, cell specific styles
    if (cellProperties.hasOwnProperty("style")) {
        styles = Object.assign({}, styles, originalStyles, cellProperties.style);
    }

    if (cellProperties.hasOwnProperty("width")) {
        styles = Object.assign({}, styles, { width: cellProperties.width });
    }

    return styles;
}

type ICellPropertiesSelectorFactory = () => components.ColumnDefinitionProps;

const mapStateToProps = () => {
    const cellPropertiesSelector: ICellPropertiesSelectorFactory = selectors.cellPropertiesSelectorFactory();
    return (state: Store, props) => {
        return {
            cellProperties: selectors.cellPropertiesSelector(state, props),
            className: selectors.classNamesForComponentSelector(state, "Cell"),
            customComponent: selectors.customComponentSelector(state, props),
            selected: myselectors.selectedSelector(state, props),
            style: selectors.stylesForComponentSelector(state, "Cell"),
            value: selectors.cellValueSelector(state, props),
        };
    };
};

export interface ISelectionCellContainerProps extends components.ColumnDefinitionProps {
    className: string,
    value: React.Component | any,
}

export const SelectionCellContainer = (OriginalComponent: components.Cell) => compose(
    connect(mapStateToProps, { toggleSelection: toggleSelectionAction }),
    mapProps((props: components.ColumnDefinitionProps) => {
        return ({
            ...props.cellProperties.extraData,
            ...props,
            className: valueOrResult(props.cellProperties.cssClassName, props) || props.className,
            style: getCellStyles(props.cellProperties, props.style),
            value: props.customComponent ?
                <props.customComponent {...props.cellProperties.extraData} {...props} /> :
                props.value,
        })}),
)((props: ISelectionCellContainerProps) =>
    <OriginalComponent
        {...props}
    />,
);
