import * as React from 'react';
import { Dropdown, Input } from 'semantic-ui-react';
import {Tag} from "../models";
import {SyntheticEvent} from "react";

interface TagDropdownProps {
    loading: boolean;
    tags: Array<Tag>;
    onAddItem: (event: SyntheticEvent<any>, data: object) => void;
}

export class TagDropdown extends React.Component<TagDropdownProps, {}> {

    static defaultProps: TagDropdownProps = {
        tags: [],
        loading: false
    };

    render() {
        const { tags, loading, onAddItem } = this.props;
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
            />
        );
    }
}