import * as React from 'react';
// import {Filter} from 'griddle-react';
import {Search} from 'semantic-ui-react';

interface SUIFilterProps {
    setFilter: (value: string) => void;
}

interface SUIFilterState {
    
}

export class SUIFilter extends React.Component<SUIFilterProps, SUIFilterState> {
    render () {
        return (
            <Search onSearchChange={this.props.setFilter} />
        )
    }
}