import * as React from "react";
import Modal from "semantic-ui-react/dist/commonjs/modules/Modal/Modal";
import {RouteComponentProps} from "react-router-dom";

import Form, {FormProps} from "semantic-ui-react/dist/commonjs/collections/Form/Form";
import Button from "semantic-ui-react/dist/commonjs/elements/Button/Button";
import {FunctionComponent} from "react";

export interface IDeviceRenameModalProps extends RouteComponentProps<any> {

}

export const DeviceRenameModal: FunctionComponent<IDeviceRenameModalProps> = ({ history, device }: IDeviceRenameModalProps) => (
    <Modal defaultOpen closeIcon onClose={() => {
        history.goBack();
    }}>
        <Modal.Header>Rename Device</Modal.Header>
        <Modal.Content>
            <Modal.Description>
                <Form>
                    <Form.Field>
                        <label>Current Device Name</label>
                        <input type="text" name="old_device_name" value={device.attributes.device_name} readOnly />
                    </Form.Field>
                    <Form.Field>
                        <label>New Device Name</label>
                        <input type="text" name="new_device_name" />
                    </Form.Field>
                </Form>
            </Modal.Description>
        </Modal.Content>
        <Modal.Actions>
            <Button type="submit" primary>
                Rename
            </Button>
        </Modal.Actions>
    </Modal>
);
