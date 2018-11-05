import {Field, FieldConfig, FieldProps} from "formik";
import * as React from "react";
import Form, {FormProps} from "semantic-ui-react/dist/commonjs/collections/Form/Form";
import Checkbox, {CheckboxProps} from "semantic-ui-react/dist/commonjs/modules/Checkbox/Checkbox";

export type IFormikCheckbox = FieldConfig & CheckboxProps;

export const FormikCheckbox: React.SFC<IFormikCheckbox> = ({
    id, name, label, toggle,
}) => (
    <Field
        name={name}
        render={({field, form}: FieldProps) => {
            const error = form.touched[name] && form.errors[name];
            return (
                <Form.Field name={name}>
                    <Checkbox toggle={toggle}
                              id={id || `field_checkbox_${field.name}`}
                              label={label}
                              name={field.name}
                              checked={field.value}
                              onChange={field.onChange}
                              />
                    {error ? (
                        <span className="sui-error-message">{form.errors[name]}</span>
                    ) : null}
                </Form.Field>
            );
        }}
    />
);
