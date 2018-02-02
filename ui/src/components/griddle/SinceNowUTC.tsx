import {distanceInWordsToNow} from "date-fns";
import * as React from "react";

interface IGriddleValue {
    griddleKey: number;
    value: any;
}

export const SinceNowUTC = (value: IGriddleValue): JSX.Element => {
    return <span>{distanceInWordsToNow(value.value)}</span>;
};
