import * as React from 'react';

export const SimpleLayout = ({ Table, Pagination, Filter, SettingsWrapper }) => (
    <div>
        <Filter />
        <Table />
        <Pagination />
    </div>
);