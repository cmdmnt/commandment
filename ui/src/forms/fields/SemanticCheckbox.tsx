import * as React from "react";
import {ChangeEvent} from "react";
import {StatelessComponent} from "react-redux";
import {WrappedFieldProps} from "redux-form";
import Form, {FormComponent, FormProps} from "semantic-ui-react/src/collections/Form";

interface IFieldProps extends WrappedFieldProps<any> {
    label: string;
    options: Array<{ key: string; value: string; text: string }>;
}

export const SemanticCheckbox: StatelessComponent<IFieldProps> = ({ input, meta: { touched, error, warning }, label, options }) => (
    <Form.Checkbox
        {...input}
        label={label}
        error={touched && !!error}
        options={options}
        onChange={(e: React.SyntheticEvent<any>, { value }: { value: ChangeEvent<any> }) => input.onChange(value)}
    />
);
