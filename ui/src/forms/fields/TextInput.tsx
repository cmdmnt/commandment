import * as React from 'react';
import {WrappedFieldProps} from "redux-form";
import {StatelessComponent} from "react-redux";

export const textInput: StatelessComponent<WrappedFieldProps<any>> = ({ input, label, type, meta: { touched, error, warning } }) => (
    <div>
        <label htmlFor={input.id}>{label} <small>{input.tooltip}</small></label>
            <input {...input} placeholder={label} type={type}/>
            {touched && ((error && <span className='error'>{error}</span>) || (warning && <span className='warning'>{warning}</span>))}
    </div>
);