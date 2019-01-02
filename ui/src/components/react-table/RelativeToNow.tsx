import {distanceInWordsToNow, parse} from "date-fns";
import * as React from "react";
import {CellInfo} from "react-table";

export const RelativeToNow: React.FunctionComponent<CellInfo> = ({ value, original }) => (
    <span>{value ? distanceInWordsToNow(parse(value), {addSuffix: true}) : ""}</span>
);
