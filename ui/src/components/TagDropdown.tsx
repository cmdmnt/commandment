import * as React from "react";
import {SyntheticEvent} from "react";
import {JSONAPIDataObject} from "../store/json-api";
import {Tag} from "../store/tags/types";

import Dropdown, { DropdownProps } from "semantic-ui-react/src/modules/Dropdown";

// Not exported by Dropdown
interface IDropdownOnSearchChangeData extends DropdownProps {
    searchQuery: string;
}

interface ITagDropdownProps {
    loading: boolean;
    tags: Array<JSONAPIDataObject<Tag>>;
    value?: any[];
    onAddItem: (event: SyntheticEvent<any>, data: object) => void;
    onSearch: (value: string) => void;
    onChange: (event: SyntheticEvent<any>, values: string[]) => void;
    searchTimeout: number;
}

interface ITagDropdownState {
    value?: string;
}

export class TagDropdown extends React.Component<ITagDropdownProps, ITagDropdownState> {

    private timeout: number;

    constructor(props: ITagDropdownProps) {
        super(props);
        this.state = {
            value: "",
        };
    }

    public render() {
        const { tags, loading, onAddItem, value, onChange } = this.props;

        const options = tags.map((item: JSONAPIDataObject<Tag>) => {
            return {
                key: item.id,
                label: { color: item.attributes.color, empty: true, circular: true },
                text: item.attributes.name,
                value: item.id,
            };
        });

        return (
            <Dropdown placeholder="Add Tag(s)"
                      multiple
                      allowAdditions
                      additionLabel="Create new tag "
                      search
                      selection
                      loading={loading}
                      options={options}
                      onAddItem={onAddItem}
                      onSearchChange={this.handleSearchChange}
                      onChange={onChange}
                      value={value}
            />
        );
    }

    private performSearch = () => {
        console.log("perform search");
        this.props.onSearch(this.state.value);
    };

    private handleSearchChange = (event: React.SyntheticEvent<HTMLElement>, data: IDropdownOnSearchChangeData): void => {
        console.log("change");
        if (this.timeout) { clearTimeout(this.timeout); }
        this.setState({ value: data.searchQuery });

        if (data.length > 0) {
            this.timeout = window.setTimeout(this.performSearch, 400);
        }
    };
}
