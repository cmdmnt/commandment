/// <reference path="../../typings/griddle.d.ts"/>
import * as React from 'react';

export const SimpleLayout = ({ Table, Pagination, Filter, SettingsWrapper }: { Table: any; Pagination: any; Filter: any; SettingsWrapper: any; }) => (
    <div>
        <Filter />
        <Table />
        <Pagination />
    </div>
);