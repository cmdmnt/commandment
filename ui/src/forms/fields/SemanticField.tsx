import * as React from "react";
import {SyntheticEvent} from "react";
import {StatelessComponent} from "react-redux";
import {WrappedFieldProps} from "redux-form";
import Form, {FormComponent, FormProps} from "semantic-ui-react/src/collections/Form";

interface IFieldProps extends WrappedFieldProps<any> {
    label: string;
    type: string;
    id: string;
    required: boolean;
    inline: boolean;
    control: any;
    placeholder: string;
}

export const SemanticField: StatelessComponent<IFieldProps> = ({
   input, label, type, meta: { touched, error, warning }, id, required, inline, control, placeholder }) => (
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
