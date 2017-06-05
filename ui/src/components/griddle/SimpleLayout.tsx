import * as React from 'react';

interface LayoutProps {
    Table: any;
    Pagination: any;
    Filter: any;
    SettingsWrapper: any;
}

export const SimpleLayout = ({ Table, Pagination, Filter, SettingsWrapper }: LayoutProps) => (
    <div>
        <Filter />
        <Table />
        <Pagination />
    </div>
);