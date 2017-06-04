import * as React from 'react';
import {WrappedFieldProps} from "redux-form";
import {StatelessComponent} from "react-redux";
import {Form} from 'semantic-ui-react';

interface FieldProps extends WrappedFieldProps<any> {
    label: string;
    options: Array<{ key: string; value: string; text: string }>;
}

export const SemanticUISelect: StatelessComponent<FieldProps> = ({ input, meta: { touched, error, warning }, label, options }) => (
    <Form.Select
        {...input}
        label={label}
        error={touched && !!error}
        options={options}
        onChange={(e: React.SyntheticEvent<any>, { value }: { value: string }) => input.onChange(value)}
    />
);
