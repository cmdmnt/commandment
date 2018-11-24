import * as React from "react";

interface ILayoutProps {
    Table: any;
    Pagination: any;
    Filter: any;
    SettingsWrapper: any;
}

export const SimpleLayout = ({ Table, Pagination, Filter, SettingsWrapper }: ILayoutProps) => (
    <div>
        <Filter />
        <Table />
        <Pagination />
    </div>
);
