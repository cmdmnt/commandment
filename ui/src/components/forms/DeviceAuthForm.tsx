import {Field, Form as FormikForm, Formik, FormikBag, FormikErrors, FormikProps, withFormik} from "formik";
import * as React from "react";
import * as Yup from "yup";
import {Organization} from "../../store/organization/types";

import {
    Button,
    Divider,
    Label,
    Radio,
    Form,
    Grid,
    Message,
    Header,
    Icon,
    Segment,
    Checkbox,
    Item
} from "semantic-ui-react";

import {SCEPConfiguration} from "../../store/configuration/types";

export interface IDeviceAuthFormValues extends SCEPConfiguration {
    authentication_method: string;
}

export interface IDeviceAuthFormProps {
    data?: SCEPConfiguration;
    loading: boolean;
    activeIndex: number;
    onSubmit: (values: IDeviceAuthFormValues) => void;
}

const initialValues: IDeviceAuthFormValues = {
    authentication_method: "internalscep",
    key_size: "1024",
    retries: 3,
    retry_delay: 10,
};

const BaseForm = (props: FormikProps<IDeviceAuthFormValues>) => {
    const { touched, errors, isSubmitting, handleChange,
        handleBlur, values, handleSubmit } = props;

    return (
        <Form onSubmit={handleSubmit}>
            <Grid columns={3} relaxed>
                <Grid.Column>
                    <Item>
                        <Item.Content>
                            <Item.Header>
                                <Form.Field>
                                    <Radio
                                        id="authentication-method-internalscep"
                                        label="Internal SCEP"
                                        name="authentication_method"
                                        value="internalscep"
                                        checked={values.authentication_method === "internalscep"}
                                        onChange={handleChange} onBlur={handleBlur}
                                    />
                                    {errors.authentication_method &&
                                    touched.authentication_method &&
                                    <Label pointing>{errors.authentication_method}</Label>}
                                </Form.Field>
                            </Item.Header>
                        </Item.Content>
                    </Item>
                </Grid.Column>
                <Grid.Column>
                    <Item>
                        <Item.Content>
                            <Item.Header>
                                <Form.Field>
                                    <Radio
                                        id="authentication-method-internalca"
                                        label="Internal CA"
                                        name="authentication_method"
                                        value="internalca"
                                        checked={values.authentication_method === "internalca"}
                                        onChange={handleChange} onBlur={handleBlur}
                                    />
                                    {errors.authentication_method &&
                                    touched.authentication_method &&
                                    <Label pointing>{errors.authentication_method}</Label>}
                                </Form.Field>
                            </Item.Header>
                            <Item.Description>Issue PKCS#12 certificates directly from the MDM.</Item.Description>
                        </Item.Content>
                    </Item>
                </Grid.Column>
                <Grid.Column>
                    <Item>
                        <Item.Content>
                            <Item.Header>
                                <Form.Field>
                                    <Radio
                                        id="authentication-method-externalscep"
                                        label="External SCEP"
                                        name="authentication_method"
                                        value="externalscep"
                                        checked={values.authentication_method === "externalscep"}
                                        onChange={handleChange} onBlur={handleBlur}
                                    />
                                </Form.Field>
                            </Item.Header>
                            <Item.Description>
                                Use an external SCEP service to issue certificates such as Microsoft NDES.
                            </Item.Description>
                            <Segment disabled={values.authentication_method !== "externalscep"}>
                                <Form.Field>
                                    <label>URL</label>
                                    <input id="url" name="url" type="url"
                                           value={values.url}
                                           placeholder="http://scep.example.com/scep"
                                           onChange={handleChange} onBlur={handleBlur}
                                           required />
                                    {errors.url &&
                                    touched.url &&
                                    <Label pointing>{errors.url}</Label>}
                                </Form.Field>
                                {/*<Form.Field>*/}
                                    {/*<small className="float-right">*/}
                                        {/*Optional. Any string that is understood by the SCEP server.*/}
                                    {/*</small>*/}
                                    {/*<label>Name</label>*/}
                                    {/*<input id="name" name="name" type="text"*/}
                                           {/*onChange={handleChange} onBlur={handleBlur}*/}
                                           {/*placeholder="CA-NAME or organization.org"/>*/}
                                    {/*{errors.name &&*/}
                                    {/*touched.name &&*/}
                                    {/*<Label pointing>{errors.name}</Label>}*/}
                                {/*</Form.Field>*/}
                                <Form.Field>
                                    <label>Challenge</label>
                                    <input id="challenge" name="challenge"
                                           onChange={handleChange} onBlur={handleBlur}
                                           type="password" />
                                    {errors.challenge &&
                                    touched.challenge &&
                                    <Label pointing>{errors.challenge}</Label>}
                                </Form.Field>
                                <small className="float-right">
                                    Optional. Used as the pre-shared secret for automatic enrollment
                                </small>
                            </Segment>
                        </Item.Content>
                    </Item>
                </Grid.Column>
            </Grid>

            <h2>Certificate Requests</h2>
            <Message attached>These details explain what kind of information is included in device
                certificates.</Message>
            <Segment attached>
                <Form.Field>
                    <label>Subject</label>
                    <input type="text" id="subject" name="subject"
                           onChange={handleChange} onBlur={handleBlur} value={values.subject}
                           placeholder="O=Commandment/OU=IT/CN=%HardwareUUID%" />
                </Form.Field>
                <Header size="tiny">Key size (in bits)</Header>

                <Form.Field>
                    <Radio label="1024 bits"
                           id="key-size-1024"
                           name="key_size"
                           value="1024"
                           checked={values.key_size === "1024"}
                           onChange={handleChange} onBlur={handleBlur}
                    />
                </Form.Field>
                <Form.Field>
                    <Radio label="2048 bits"
                           id="key-size-2048"
                           name="key_size"
                           value="2048"
                           checked={values.key_size === "2048"}
                           onChange={handleChange} onBlur={handleBlur}
                    />
                </Form.Field>

                <Header size="tiny">Use SCEP key for</Header>

                <Form.Field>
                    <Checkbox label="Signing" value="1" onChange={handleChange} onBlur={handleBlur} />
                </Form.Field>
                <Form.Field>
                    <Checkbox label="Encryption" value="4" onChange={handleChange} onBlur={handleBlur} />
                </Form.Field>

                <Form.Field>
                    <label>Retries</label>
                    <input type="number" id="retries" name="retries" value={values.retries}
                           onChange={handleChange} onBlur={handleBlur} />
                    <p>The number of times the device should retry if the server sends a PENDING response</p>
                </Form.Field>

                <Form.Field>
                    <label>Retry Delay</label>
                    <input type="number" id="retry_delay" name="retry_delay" value={values.retry_delay}
                           onChange={handleChange} onBlur={handleBlur} />
                    <p>The number of seconds to wait between subsequent retries. The first retry is attempted without
                        this delay</p>
                </Form.Field>
            </Segment>
        </Form>
    );
};

export const DeviceAuthForm = withFormik<IDeviceAuthFormProps, IDeviceAuthFormValues>({
    handleSubmit: (values, formikBag: FormikBag<IDeviceAuthFormProps, IDeviceAuthFormValues>) => {
        formikBag.props.onSubmit(values);
        formikBag.setSubmitting(false);
    },
    mapPropsToValues: (props) => {
        return props.data || initialValues;
    },
    validationSchema: Yup.object().shape({

    }),
    enableReinitialize: true,
    displayName: "DeviceAuthForm",
})(BaseForm);
