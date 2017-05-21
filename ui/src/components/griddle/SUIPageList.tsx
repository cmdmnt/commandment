import * as React from 'react';
import {Table, Menu, Icon} from 'semantic-ui-react';

interface SUIPageListProps {
    maxPages: number;
    currentPage: number;
    setPage: (pageNumber: number) => void;
}

export class SUIPageList extends React.Component<SUIPageListProps, undefined> {
    render() {
        const {
            maxPages,
            currentPage,
            setPage,
            previous: Previous,
            next: Next
        } = this.props;

        const pages = [];
        for (let x = 0; x < maxPages; x++) {
            pages.push(<Menu.Item as='a' onClick={() => { this.props.dispatch(setPage(x+1)) }}>{x+1}</Menu.Item>);
        }
        
        return (
            <Menu floated='right' pagination>
                <Previous />
                {pages}
                <Next />
            </Menu>
        );
    }
}