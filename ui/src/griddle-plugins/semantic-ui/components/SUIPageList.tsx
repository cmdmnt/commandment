import * as React from 'react';
import Menu from "semantic-ui-react/src/collections/Menu";
import {Dispatch} from 'react-redux';
import {Action} from 'redux';

interface SUIPageListProps {
    maxPages: number;
    currentPage: number;
    setPage: (pageNumber: number) => Action;
    previous: any;
    next: any;
    dispatch: Dispatch<any>;
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
            pages.push(<Menu.Item
                key={'page-'+(x+1)}
                as='a'
                active={x+1 == currentPage}
                onClick={() => { this.props.dispatch(setPage(x+1)) }}>{x+1}</Menu.Item>);
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