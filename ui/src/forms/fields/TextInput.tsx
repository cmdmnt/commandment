import * as React from 'react';
import {WrappedFieldProps} from "redux-form";
import {StatelessComponent} from "react-redux";

interface FieldProps extends WrappedFieldProps<any> {
    label: string;
    type: string;
    id: string;
    tooltip: string;
}

export const textInput: StatelessComponent<FieldProps> = ({ input, label, type, meta: { touched, error, warning }, id, tooltip }) => (
    <div>
        <label htmlFor={id}>{label} <small>{tooltip}</small></label>
        <input {...input} placeholder={label} type={type}/>
        {touched && ((error && <span className='error'>{error}</span>) || (warning && <span className='warning'>{warning}</span>))}
    </div>
);