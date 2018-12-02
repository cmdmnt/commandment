import * as React from "react";
import { compose } from "recompose";
import {components} from "griddle-react";

export const SelectionCellEnhancer = (OriginalComponent: components.Cell) => compose(

)((props) => <OriginalComponent {...props} />);
