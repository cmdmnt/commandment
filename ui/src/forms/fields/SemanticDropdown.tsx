import * as React from 'react';
import {WrappedFieldProps} from "redux-form";
import {StatelessComponent} from "react-redux";
import {Form} from 'semantic-ui-react';

interface FieldProps extends WrappedFieldProps<any> {
    label: string;
    type: string;
    id: string;
    tooltip: string;
}

export const SemanticDropdown: StatelessComponent<FieldProps> = ({ input, label, type, meta: { touched, error, warning }, id, tooltip, children }) => (
    <Form.Dropdown {...input} label={label} error={touched && !!error}>
    </Form.Dropdown>
);