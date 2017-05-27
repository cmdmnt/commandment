import * as React from 'react';
import {Input} from 'semantic-ui-react';

interface SUIFilterProps {
    setFilter: (value: string) => void;
    searchTimeoutMs: number;
}

interface SUIFilterState {
    value: string;
}

export class SUIFilter extends React.Component<SUIFilterProps, SUIFilterState> {

    _timeout: number;

    static defaultProps = {
        searchTimeoutMs: 400
    };

    constructor(props: SUIFilterProps) {
        super(props);
        this._timeout = null;
        this.state = {value: ''};
    }

    performSearch = () => {
        console.log('perform search');
        this.props.setFilter(this.state.value);
    };

    searchTimeout = (e: any) => {
        this.setState({ value: e.target.value });

        if (this._timeout) {
            clearTimeout(this._timeout);
        }

        this._timeout = setTimeout(this.performSearch, this.props.searchTimeoutMs);
    };


    render () {
        return (
            <Input
                icon='search'
                placeholder='Search...'
                value={this.state.value}
                onChange={this.searchTimeout} />
        )
    }
}