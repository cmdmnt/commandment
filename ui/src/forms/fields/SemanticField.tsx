import * as React from 'react';
import {WrappedFieldProps} from "redux-form";
import {StatelessComponent} from "react-redux";
import * as Form from 'semantic-ui-react/dist/es/collections/Form';
import {SyntheticEvent} from "react";

interface FieldProps extends WrappedFieldProps<any> {
    label: string;
    type: string;
    id: string;
    required: boolean;
    inline: boolean;
    control: any;
    placeholder: string;
}

export const SemanticField: StatelessComponent<FieldProps> = ({ input, label, type, meta: { touched, error, warning }, id, required, inline, control, placeholder }) => (
    <Form.Field
        id={id}
        {...input}
        control={control}
        label={label}
        type={type}
        error={touched && !!error}
        required={required}
        inline={inline}
        placeholder={placeholder}
        onChange={(e: SyntheticEvent<any>, { value }: { value: any }) => input.onChange(value)}
    />
);