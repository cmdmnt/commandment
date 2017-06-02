import * as React from 'react';
import { Dropdown, Input } from 'semantic-ui-react';
import {Tag} from "../models";

interface TagDropdownProps {
    loading: boolean;
    tags: Array<Tag>;
}

export class TagDropdown extends React.Component<TagDropdownProps, {}> {

    static defaultProps: TagDropdownProps = {
        tags: [],
        loading: true
    };

    render() {
        const { tags, loading } = this.props;
        return (
            <Dropdown text='Tag'
                      search
                      floating
                      labeled
                      button
                      className='icon'
                      icon='tags'
                      options={tags}
            />
        );
    }
}