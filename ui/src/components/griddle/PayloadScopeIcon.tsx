import * as React from "react";

interface IGriddleValue {
    griddleKey: number;
    value: any;
}

export const PayloadScopeIcon = (value: IGriddleValue): JSX.Element => {
    const icons: { [propName: string]: string; } = {
       System: "fa-computer",
       User: "fa-user",
    };

    return <i className={"fa " + icons[value.value]} />;
};
