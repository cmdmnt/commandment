import * as React from 'react';
import {ComponentDecorator} from "react-redux";
import {Griddle, SortProperties} from "griddle-react";
import {FlaskFilters} from "../actions/constants";

interface GriddleDecorator {
    <P, S>(WrappedComponent: React.Component<P, S>): React.Component<P, S & GriddleDecoratorState>;
}

export interface GriddleDecoratorState {
    currentPage: number;
    pageSize: number;
    filter: string;
    sortColumnId: string;
}

/**
 * This higher order component for Griddle wraps an existing component to provide handlers for paging, filtering and sorting.
 * @param WrappedComponent
 * @returns React.Component
 */
export const griddle: GriddleDecorator = (WrappedComponent: React.Component<any, any>) => {
    class GriddleDecorator extends React.Component<any, GriddleDecoratorState> {

        displayName: string;

        constructor(props: any) {
            super(props);
            this.state = {
                currentPage: 1,
                pageSize: 20,
                filter: '',
                sortColumnId: ''
            }
        }

        handleNext = () => {
            this.setState({ currentPage: this.state.currentPage + 1 });
        };

        handlePrevious = () => {
            this.setState({ currentPage: this.state.currentPage - 1 });
        };

        handleGetPage = (pageNumber: number) => {
            this.setState({ currentPage: pageNumber });
        };

        handleFilter = (value: string) => {
            this.setState({ filter: value });
        };

        handleSort = (sortProperties: { id: string }) => {
            this.setState({ sortColumnId: sortProperties.id });
        };

        render() {
            return <WrappedComponent {...this.props}
                                     griddleState={this.state}
                                     events={{
                onNext: this.handleNext,
                onPrevious: this.handlePrevious,
                onGetPage: this.handleGetPage,
                onSort: this.handleSort,
                onFilter: this.handleFilter
            }} />;
        }
    }

    let wrappedDisplayName = WrappedComponent.displayName || WrappedComponent.name || 'Component';
    GriddleDecorator.displayName = `GriddleDecorator(${wrappedDisplayName})`;
    return GriddleDecorator;
};
