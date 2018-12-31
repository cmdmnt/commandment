import * as React from "react";
import Dropdown from "semantic-ui-react/src/modules/Dropdown/Dropdown";

export enum UIActionTypes {
    BLANK_PUSH = "BLANK_PUSH",
    CLEAR_PASSCODE = "CLEAR_PASSCODE",
    FULL_INVENTORY = "FULL_INVENTORY",
}

export interface IActionMenu {
    enabledActions: UIActionTypes[];
}

export const ActionMenu: React.FunctionComponent = (props: IActionMenu) => (
    <Dropdown inline button text="action" onChange={this.handleAction} options={[
        {text: "Force Push", value: "push"},
        {text: "Inventory", value: "inventory"},
        {text: "Test", value: "test"},
    ]}></Dropdown>
);
