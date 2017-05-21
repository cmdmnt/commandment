import * as React from 'react';

interface SUIPaginationProps {
    Next: React.ComponentClass;
    Previous: React.ComponentClass;
    PageDropdown: React.ComponentClass;
}

export const SUIPagination = ({ Next, Previous, PageDropdown }: SUIPaginationProps) => (
    <PageDropdown previous={Previous} next={Next} />
);
