import * as React from 'react';
import {Field, reduxForm, FormProps} from 'redux-form';
import {Header, Icon, Segment, Message, Divider, Grid, Form} from 'semantic-ui-react';
import {SemanticInput} from "../fields/SemanticInput";

export interface FormData {
    stoken: string;
}

interface VPPFormProps extends FormProps<FormData, any, any> {
    loading: boolean;
    submitted: boolean;
}

export class UnconnectedVPPForm extends React.Component<VPPFormProps, undefined> {
    static defaultProps = {
        loading: false
    };

    render() {
        const {
            handleSubmit,
            pristine,
            reset,
            submitting,
            submitted,
            loading
        } = this.props;

        return (
            <Form onSubmit={handleSubmit} loading={loading} success={pristine && submitted}>
                <Segment>
                    <Field id="stoken" name="stoken" type="file" component={SemanticInput} />
                </Segment>
                <Form.Button type="submit" primary disabled={false}>Save</Form.Button>
            </Form>
        )
    }
}

export const VPPForm = reduxForm<FormData, VPPFormProps, undefined>({
    form: 'organization'
})(UnconnectedVPPForm);
