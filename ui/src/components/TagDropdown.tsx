import * as React from "react";
import Input from "semantic-ui-react/src/elements/Input";
import Dropdown, { DropdownProps } from "semantic-ui-react/src/modules/Dropdown";
import { DropdownItemProps } from "semantic-ui-react/src/modules/Dropdown/DropdownItem";

import {SyntheticEvent} from "react";
import {Tag} from "../models";

// Not exported by Dropdown
interface DropdownOnSearchChangeData extends DropdownProps {
    searchQuery: string;
}

interface TagDropdownProps {
    loading: boolean;
    tags: DropdownItemProps[];
    value?: any[];
    onAddItem: (event: SyntheticEvent<any>, data: object) => void;
    onSearch: (value: string) => void;
    onChange: (event: SyntheticEvent<any>, values: string[]) => void;
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
            value: "",
        };
    }

    performSearch = () => {
        console.log("perform search");
        this.props.onSearch(this.state.value);
    }

    handleSearchChange = (event: React.SyntheticEvent<HTMLElement>, data: DropdownOnSearchChangeData): void => {
        console.log("change");
        if (this._timeout) { clearTimeout(this._timeout); }
        this.setState({ value: data.searchQuery });

        if (data.length > 0) {
            this._timeout = window.setTimeout(this.performSearch, 400);
        }
    }

    render() {
        const { tags, loading, onAddItem, value } = this.props;

        return (
            <Dropdown placeholder="Add Tag(s)"
                      multiple
                      allowAdditions
                      additionLabel="Add new tag "
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
