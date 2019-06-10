import * as React from "react";
import {Input, Dropdown} from "semantic-ui-react";
import {JSONAPIDataObject} from "../../store/json-api";
import {Tag} from "../../store/tags/types";
import {ActionMenu} from "../ActionMenu";

export interface ISUISelectionTools {
    loading: boolean;
    selectionCount: number;
    tags: Array<JSONAPIDataObject<Tag>>;
}

export const SUISelectionTools: React.FunctionComponent<ISUISelectionTools> = (props: ISUISelectionTools) => (
    <div>
        <Dropdown text="Tag device(s)" icon="filter" floating labeled button className="icon" disabled={props.selectionCount < 1}>
            <Dropdown.Menu>
                <Input icon="search" iconPosition="left" className="search" />
                <Dropdown.Divider />
                <Dropdown.Header icon="tags" content="Tag Label" />
                <Dropdown.Menu scrolling>
                    {props.tags && props.tags.map((tag) =>
                        <Dropdown.Item key={tag.id}
                                       value={tag.id}
                                       text={tag.attributes.name}
                                       label={{ color: tag.attributes.color, empty: true, circular: true }}/>)}
                </Dropdown.Menu>
            </Dropdown.Menu>
        </Dropdown>

        <ActionMenu enabledActions={["BLANK_PUSH"]}/>
    </div>
);
