import {distanceInWordsToNow} from "date-fns";
import * as React from "react";

interface IGriddleValue {
    griddleKey: number;
    value: any;
}

export const SinceNowUTC = (value: IGriddleValue): JSX.Element => {
    return <span>{value.value ? distanceInWordsToNow(value.value, {addSuffix: true}) : ''}</span>;
};
