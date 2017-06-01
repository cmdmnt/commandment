import * as React from 'react';
import {WrappedFieldProps} from "redux-form";
import {StatelessComponent} from "react-redux";
import {Input, Form} from 'semantic-ui-react';

interface FieldProps extends WrappedFieldProps<any> {
    label: string;
    type: string;
    id: string;
    tooltip: string;
    required: boolean;
    width: number;
}

export const SemanticInput: StatelessComponent<FieldProps> = ({ input, label, type, meta: { touched, error, warning }, id, tooltip, required, width }) => (
    <Form.Input fluid {...input} label={label} type={type} error={touched && !!error} required={required} width={width} />
);