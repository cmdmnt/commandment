import * as React from 'react';
import {Field, reduxForm, FormProps} from 'redux-form';

import {required, reverseDns} from "../../validations";

import Form from "semantic-ui-react/src/collections/Form";
import Grid from "semantic-ui-react/src/collections/Grid";
import Header from "semantic-ui-react/src/elements/Header";
import Icon from "semantic-ui-react/src/elements/Icon";
import Message from "semantic-ui-react/src/collections/Message";
import Segment from "semantic-ui-react/src/elements/Segment";
import Divider from "semantic-ui-react/src/elements/Divider";

import {SemanticInput} from "../fields/SemanticInput";
import {SemanticUISelect} from "../fields/SemanticUISelect";

export interface FormData {
    name: string;
    payload_prefix: string;
    x509_ou: string;
    x509_o: string;
    x509_st: string;
    x509_c: string;
}

interface OrganizationFormProps extends FormProps<FormData, any, any> {
    loading: boolean;
    submitted: boolean;
}


export class UnconnectedOrganizationForm extends React.Component<OrganizationFormProps, undefined> {

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
                <Message attached>These details are shown in configuration profiles</Message>
                <Segment attached>
                    <Header as='h3'><Icon name='home'/> General Information</Header>
                    
                    <small className='float-right'>The name of your organization</small>
                    <Field name='name' component={SemanticInput} label='Name' type='text' placeholder='Acme Inc.'
                           id='name'
                           required validate={required}/>

                    <small className='float-right'>reverse style DNS name of your organization</small>
                    <Field name='payload_prefix' component={SemanticInput} label='Prefix' type='text'
                           placeholder='com.acme'
                           id='payload-prefix' validate={[required, reverseDns]} required/>
                </Segment>

                <Message attached>These details will be shown on any certificates issued by the MDM</Message>
                <Segment attached>
                    <Header as='h3'><Icon name='certificate'/> Certificate Details</Header>
                    
                    <Grid columns={2}>
                        <Grid.Column>
                            <Field name='x509_ou' component={SemanticInput}
                                   type='text' label='OU or Department' id='x509ou' placeholder='IT'/>
                        </Grid.Column>
                        <Grid.Column>
                            <Field name='x509_o' component={SemanticInput}
                                   type='text' label='Organization Name' id='x509o' placeholder='Acme'/>
                        </Grid.Column>
                    </Grid>
                    <Grid columns={2}>
                        <Grid.Column>
                            <Field name='x509_st' label='State or Province' component={SemanticInput}
                                   type='text' id='x509-st'/>
                        </Grid.Column>
                        <Grid.Column>
                            <Field name='x509_c'
                                   label='Country Code'
                                   component={SemanticUISelect}
                                   id='x509-c'
                                   options={[
                                       { key: 'au', text: 'Australia', value: 'AU' },
                                       { key: 'us', text: 'United States', value: 'US' }
                                   ]}
                            >
                            </Field>
                        </Grid.Column>
                    </Grid>

                    <Message
                        success
                        header='Form Completed'
                        content="Organization details saved"
                    />
                    <Divider hidden />

                    <Form.Group>
                        <Form.Button type='button' disabled={pristine || submitting} onClick={reset}>
                            Revert
                        </Form.Button>
                        <Form.Button type='submit' disabled={pristine || submitting} primary>
                            Save
                        </Form.Button>
                    </Form.Group>
                </Segment>
            </Form>
        )
    }
}

export const OrganizationForm = reduxForm<FormData, OrganizationFormProps, undefined>({
    form: 'organization'
})(UnconnectedOrganizationForm);
