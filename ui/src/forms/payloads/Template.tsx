import * as React from 'react';
import {Field, reduxForm, FormProps} from 'redux-form';

export interface FormData {

}

interface PayloadFormProps extends FormProps<FormData, any, any> {

}

@reduxForm<FormData, PayloadFormProps, undefined>({
    form: 'payload'
})
export class PayloadForm extends React.Component<PayloadFormProps, undefined> {
    render() {
        const {
            handleSubmit
        } = this.props;

        return (
            <form onSubmit={handleSubmit}>
                <div className='row'>
                    <div className='column'>
                    </div>
                </div>
            </form>
        )
    }
}