import * as React from 'react';

interface SUIPaginationProps {
    Next: React.ComponentClass<any>;
    Previous: React.ComponentClass<any>;
    PageDropdown: React.ComponentClass<any>;
}

export const SUIPagination = ({ Next, Previous, PageDropdown }: SUIPaginationProps) => (
    <PageDropdown previous={Previous} next={Next} />
);
