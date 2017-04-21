import * as React from 'react';
import {Field, reduxForm, FormProps} from 'redux-form';

import './OrganizationForm.scss';
import {required, reverseDns} from "../validations";
import {textInput} from "./fields/TextInput";

export interface FormData {
    name: string;
    payload_prefix: string;
    x509_ou: string;
    x509_o: string;
    x509_st: string;
    x509_c: string;
}

interface OrganizationFormProps extends FormProps<FormData, any, any> {

}

@reduxForm<FormData, OrganizationFormProps, undefined>({
    form: 'organization'
})
export class OrganizationForm extends React.Component<OrganizationFormProps, undefined> {
    render() {
        const {
            handleSubmit,
            pristine,
            reset,
            submitting
        } = this.props;

        return (
            <form onSubmit={handleSubmit}>
                <fieldset className='top-margin'>
                    <h3><i className='fa fa-home' /> General Information</h3>
                    <blockquote>These details are shown in configuration profiles</blockquote>
                    <label htmlFor='name'>Name <small className='float-right'>The name of your organization</small></label>
                    <Field name='name' component={textInput} type='text' placeholder='Acme Inc.' id='name'
                           required validate={required} />


                    <label htmlFor='payload-prefix'>Prefix <small className='float-right'>reverse style DNS name of your organization</small></label>
                    <Field name='payload_prefix' component={textInput} type='text' placeholder='com.acme'
                           id='payload-prefix' validate={[required, reverseDns]} required />
                </fieldset>
                <hr />
                <fieldset>

                    <h3><i className='fa fa-certificate' /> Certificate Details</h3>
                    <blockquote>These details will be shown on any certificates issued by the MDM</blockquote>

                    <div className='row'>
                        <div className='column'>
                            <label htmlFor='x509ou'>OU or Department</label>
                            <Field name='x509_ou' component='input' type='text' id='x509ou' placeholder='IT' />
                        </div>
                        <div className='column'>
                            <label htmlFor='x509o'>Organization Name</label>
                            <Field name='x509_o' component='input' type='text' id='x509o' placeholder='Acme' />
                        </div>
                    </div>
                    <div className='row'>
                        <div className='column'>
                            <label htmlFor='x509-st'>State or Province</label>
                            <Field name='x509_st' component='input' type='text' id='x509-st' />
                        </div>
                        <div className='column'>
                            <label htmlFor='x509-c'>Country</label>
                            <Field name='x509_c' component='select' id='x509-c'>
                                <option value='US'>United States</option>
                                <option value='AU'>Australia</option>
                            </Field>
                        </div>
                    </div>

                </fieldset>
                <div className='row'>
                    <div className='column clearfix'>
                        <button type='button' disabled={pristine || submitting} className='float-left button-outline' onClick={reset}>
                            Undo Changes
                        </button>
                        <button type='submit' disabled={pristine || submitting} className="float-right button-primary">
                            Save
                        </button>
                    </div>
                </div>

            </form>
        )
    }
}