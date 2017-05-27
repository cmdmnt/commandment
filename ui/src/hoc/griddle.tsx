import * as React from 'react';
import {ComponentDecorator} from "react-redux";

interface GriddleDecorator {
    (): void;
}


export const griddle: ComponentDecorator = (WrappedComponent: React.Component) => {
    return class extends React.Component {

    }
};
