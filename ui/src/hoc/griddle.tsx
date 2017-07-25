import * as React from 'react';

interface GriddleDecoratorFactory {
    <P>(WrappedComponent: React.ComponentClass<P>): React.ComponentClass<P>;
}

export interface GriddleDecoratorState {
    currentPage: number;
    pageSize: number;
    filter: string;
    sortId: string;
    sortAscending: boolean;
}

export interface GriddleDecoratorHandlers {
    handleNext: () => void;
    handlePrevious: () => void;
    handleFilter: (value: string) => void;
    handleSort: (sortProperties: { id: string }) => void;
}

/**
 * This higher order component for Griddle wraps an existing component to provide handlers for paging, filtering and sorting.
 * @param WrappedComponent
 * @returns React.Component
 */
export const griddle: GriddleDecoratorFactory = (WrappedComponent: React.ComponentClass<any>) => {
    class GriddleDecorator extends React.Component<any, GriddleDecoratorState> implements React.ComponentClass<{}> {

        displayName: string;

        constructor(props: any) {
            super(props);
            this.state = {
                currentPage: 1,
                pageSize: 20,
                filter: '',
                sortId: '',
                sortAscending: true
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
            const ascending = (this.state.sortId != sortProperties.id) ? true : !this.state.sortAscending;
            this.setState({ sortId: sortProperties.id, sortAscending: ascending });
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
