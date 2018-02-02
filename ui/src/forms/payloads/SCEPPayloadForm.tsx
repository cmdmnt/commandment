import * as React from "react";
import {Field, FormProps, reduxForm} from "redux-form";
import {Button, Form, Grid, Header, Icon, Input, Message, Radio, Segment} from "semantic-ui-react";
import {SemanticField} from "../fields/SemanticField";
import {SemanticInput} from "../fields/SemanticInput";

export interface FormData {
    id?: string;
    url?: string;
    name: string;
    subject: string;
    challenge: string;
    key_size: number;
    ca_fingerprint: string;
    key_usage: number;
    subject_alt_name: string;
    retries: number;
    retry_delay: number;
}

interface ISCEPPayloadFormProps extends FormProps<FormData, any, any> {
    onClickTest: (url: string) => void;
    loading: boolean;
    submitted: boolean;
}

export class UnconnectedSCEPPayloadForm extends React.Component<ISCEPPayloadFormProps, undefined> {

    public static defaultProps = {
        loading: false,
        submitted: false,
    };

    public render() {
        const {
            handleSubmit,
            loading,
            submitting,
            submitted,
            pristine,
            reset,
        } = this.props;

        return (
            <Form onSubmit={handleSubmit} loading={loading} success={submitted}>
                <Message attached>These details explain how devices will contact your SCEP server.</Message>
                <Segment attached>
                    <Form.Group>
                        <Field id="url" label="URL" name="url" component={SemanticInput} type="url"
                               placeholder="http://scep.example.com/scep" width={12} required/>
                        <Field label="CA Fingerprint" id="cafingerprint" name="ca_fingerprint" component={SemanticInput}
                               type="text" width={4} action="fetch" />
                    </Form.Group>

                    <small className="float-right">Optional. Any string that is understood by the SCEP server.</small>
                    <Field label="Name" id="name" name="name" component={SemanticInput} type="text"
                           placeholder="CA-NAME or organization.org"/>

                    <small className="float-right">Optional. Used as the pre-shared secret for automatic enrollment
                    </small>
                    <Field label="Challenge" id="challenge" name="challenge" component={SemanticInput} type="password"/>
                </Segment>

                <Message attached>These details explain what kind of information is included in device
                    certificates.</Message>
                <Segment attached>
                    <Field label="Subject" id="subject" name="subject" component={SemanticInput} type="text"
                           placeholder="O=Commandment/OU=IT/CN=%HardwareUUID%"/>
                    <Field id="subject_alt_name" name="subject_alt_name" component={SemanticInput}
                           label="SubjectAltName" type="text"/>

                    <Form.Group inline>
                        <label>Key size (in bits)</label>
                        <Field id="key_size_1024" component={SemanticField} control={Radio} type="radio" name="key_size"
                               label="1024" value="1024"/>
                        <Field id="key_size_2048" component={SemanticField} control={Radio} type="radio" name="key_size"
                               label="2048" value="2048"/>
                    </Form.Group>

                    <Form.Group inline>
                        <label>Use SCEP key for</label>
                        <Field id="key_usage_signing" name="key_usage" component={SemanticField} control={Radio}
                               type="radio" value="1" label="Signing"/>
                        <Field id="key_usage_encryption" name="key_usage" component={SemanticField} control={Radio}
                               type="radio" value="4" label="Encryption"/>
                        <Field id="key_usage_both" name="key_usage" component={SemanticField} control={Radio}
                               type="radio" value="5" label="Both"/>
                    </Form.Group>

                    <Field id="retries" label="Retries" name="retries" component={SemanticInput} type="number"/>
                    <p>The number of times the device should retry if the server sends a PENDING response</p>

                    <Field id="retry_delay" label="Retry Delay" name="retry_delay" component={SemanticInput}
                           type="number"/>
                    <p>The number of seconds to wait between subsequent retries. The first retry is attempted without
                        this delay</p>

                    <Message
                        success
                        header="Form Completed"
                        content="SCEP details saved"
                    />

                    <Form.Group>
                    <Form.Button type="button" disabled={pristine || submitting} onClick={reset}>
                        Revert
                    </Form.Button>
                    <Form.Button type="submit" primary disabled={pristine || submitting}>Save</Form.Button>
                    </Form.Group>
                </Segment>
            </Form>
        );
    }
}

export const SCEPPayloadForm = reduxForm<FormData, ISCEPPayloadFormProps, undefined>({
    form: "scep_payload",
})(UnconnectedSCEPPayloadForm);
