import * as React from 'react';
import {WrappedFieldProps} from "redux-form";
import {StatelessComponent} from "react-redux";
import {Form} from 'semantic-ui-react';

interface FieldProps extends WrappedFieldProps<any> {
    label: string;
    type: string;
    id: string;
    required: boolean;
    inline: boolean;
    control: any;
}

export const SemanticField: StatelessComponent<FieldProps> = ({ input, label, type, meta: { touched, error, warning }, id, required, inline, control }) => (
    <Form.Field id={id} {...input} control={control} label={label} type={type} error={touched && !!error} required={required} inline={inline} />
);