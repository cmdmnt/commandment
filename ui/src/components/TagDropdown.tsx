import * as React from 'react';
import {Dropdown, DropdownItemProps, Input} from 'semantic-ui-react';
import {Tag} from "../models";
import {SyntheticEvent} from "react";

interface TagDropdownProps {
    loading: boolean;
    tags: Array<DropdownItemProps>;
    value?: Array<any>;
    onAddItem: (event: SyntheticEvent<any>, data: object) => void;
    onSearch: (value: string) => void;
    onChange: (event: SyntheticEvent<any>, values: Array<string>) => void;
    searchTimeout: number;
}

interface TagDropdownState {
    value?: string;
}

export class TagDropdown extends React.Component<TagDropdownProps, TagDropdownState> {

    _timeout: number;

    constructor(props: TagDropdownProps) {
        super(props);
        this.state = {
            value: ''
        };
    }

    performSearch = () => {
        console.log('perform search');
        this.props.onSearch(this.state.value);
    };

    handleSearchChange = (event: SyntheticEvent<any>, value: string) => {
        console.log('change');
        if (this._timeout) { clearTimeout(this._timeout); }
        this.setState({ value });

        if (value.length > 0) {
            this._timeout = setTimeout(this.performSearch, 400);
        }
    };

    render() {
        const { tags, loading, onAddItem, value } = this.props;

        return (
            <Dropdown placeholder='Add Tag(s)'
                      multiple
                      allowAdditions
                      additionLabel='Add new tag '
                      search
                      selection
                      loading={loading}
                      options={tags}
                      onAddItem={onAddItem}
                      onSearchChange={this.handleSearchChange}
                      onChange={this.props.onChange}
                      value={value}
            />
        );
    }
}