import * as React from 'react';
import { connect } from 'react-redux';
import { components } from 'griddle-react'; 

export const RowEnhancer = (Row: components.Row) => {
    console.log('enhance!');

    interface RowEnhancerProps extends components.RowProps {

    }

    return class extends React.Component<RowEnhancerProps, any> {
        handleClick = () => {
            console.log('asd');
        };

        render () {
            console.dir(this.props);

            return (
                <Row onClick={this.handleClick} {...this.props} />
            )
        }
    }
};