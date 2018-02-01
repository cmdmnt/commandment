import * as React from "react";
import {ChangeEvent} from "react";
import {StatelessComponent} from "react-redux";
import {WrappedFieldProps} from "redux-form";
import {Form} from "semantic-ui-react";

interface IFieldProps extends WrappedFieldProps<any> {
    label: string;
    options: Array<{ key: string; value: string; text: string }>;
}

export const SemanticUISelect: StatelessComponent<IFieldProps> = ({ input, meta: { touched, error, warning }, label, options }) => (
    <Form.Select
        {...input}
        label={label}
        error={touched && !!error}
        options={options}
        onChange={(e: React.SyntheticEvent<any>, { value }: { value: ChangeEvent<any> }) => input.onChange(value)}
    />
);
