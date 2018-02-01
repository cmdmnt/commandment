import * as React from "react";

type GriddleDecoratorFactory = <P>(WrappedComponent: React.ComponentClass<P>) => React.ComponentClass<P>;

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
    class GriddleDecorator extends React.Component<any, GriddleDecoratorState> {

        displayName: string;

        constructor(props: any) {
            super(props);
            this.state = {
                currentPage: 1,
                filter: "",
                pageSize: 20,
                sortAscending: true,
                sortId: "",
            };
        }

        public render() {
            return <WrappedComponent {...this.props}
                                     griddleState={this.state}
                                     events={{
                                         onFilter: this.handleFilter,
                                         onGetPage: this.handleGetPage,
                                         onNext: this.handleNext,
                                         onPrevious: this.handlePrevious,
                                         onSort: this.handleSort,
                                     }} />;
        }

        protected handleNext = () => {
            this.setState({ currentPage: this.state.currentPage + 1 });
        }

        protected handlePrevious = () => {
            this.setState({ currentPage: this.state.currentPage - 1 });
        }

        protected handleGetPage = (pageNumber: number) => {
            this.setState({ currentPage: pageNumber });
        }

        protected handleFilter = (value: string) => {
            this.setState({ filter: value });
        }

        protected handleSort = (sortProperties: { id: string }) => {
            const ascending = (this.state.sortId !== sortProperties.id) ? true : !this.state.sortAscending;
            this.setState({ sortId: sortProperties.id, sortAscending: ascending });
        }
    }

    const wrappedDisplayName = WrappedComponent.displayName || "Component";
    (GriddleDecorator as React.ComponentClass<any>).displayName = `GriddleDecorator(${wrappedDisplayName})`;
    return GriddleDecorator;
};
