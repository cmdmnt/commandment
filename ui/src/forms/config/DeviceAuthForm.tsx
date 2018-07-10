import * as React from 'react';
import Form from "semantic-ui-react/src/collections/Form";
import Radio from "semantic-ui-react/src/addons/Radio";
import Item from "semantic-ui-react/src/views/Item";
import Segment from "semantic-ui-react/src/elements/Segment";
import Message from "semantic-ui-react/src/collections/Message";
import Checkbox from "semantic-ui-react/src/modules/Checkbox/Checkbox";
import {CheckboxProps} from "semantic-ui-react/src/modules/Checkbox/Checkbox";
import {SemanticInput} from "../fields/SemanticInput";
import {SemanticField} from "../fields/SemanticField";
import Header from "semantic-ui-react/src/elements/Header/Header";
import Grid from "semantic-ui-react/src/collections/Grid/Grid";

export interface IDeviceAuthFormState {
    authentication_method: string;
    key_size: string;
    retries: number;
    retry_delay: number;
}

export class DeviceAuthForm extends React.Component<void, IDeviceAuthFormState> {

    public state: IDeviceAuthFormState = {
        authentication_method: 'internalscep',
        key_size: '1024',
        retries: 3,
        retry_delay: 10
    };

    handleChangeDeviceAuthMethod = (event: React.FormEvent<HTMLInputElement>, data: CheckboxProps) => {
        this.setState({ authentication_method: ''+data.value });
    };

    handleChangeKeySize = (event: React.FormEvent<HTMLInputElement>, data: CheckboxProps) => {
        this.setState({ key_size: ''+data.value });
    };

    render() {
        return (
            <Form>
                <Grid columns={3} relaxed>
                    <Grid.Column>
                        <Item>
                            <Item.Content>
                                <Item.Header>
                                    <Form.Field>
                                        <Radio
                                            label='Internal SCEP'
                                            name='authentication_method'
                                            value='internalscep'
                                            checked={this.state.authentication_method == 'internalscep'}
                                            onChange={this.handleChangeDeviceAuthMethod}
                                        />
                                    </Form.Field>
                                </Item.Header>
                                <Item.Description>Use the built in SCEP service to issue certificates.</Item.Description>
                            </Item.Content>
                        </Item>
                    </Grid.Column>

                    <Grid.Column>
                        <Item>
                            <Item.Content>
                                <Item.Header>
                                    <Form.Field>
                                        <Radio
                                            label='Internal CA'
                                            name='authentication_method'
                                            value='internalca'
                                            checked={this.state.authentication_method == 'internalca'}
                                            onChange={this.handleChangeDeviceAuthMethod}
                                        />
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
                                            label='External SCEP'
                                            name='authentication_method'
                                            value='externalscep'
                                            checked={this.state.authentication_method == 'externalscep'}
                                            onChange={this.handleChangeDeviceAuthMethod}
                                        />
                                    </Form.Field>
                                </Item.Header>
                                <Item.Description>
                                    Use an external SCEP service to issue certificates such as Microsoft NDES.
                                </Item.Description>
                                <Segment disabled={this.state.authentication_method !== 'externalscep'}>
                                    <Form.Field>
                                        <label>URL</label>
                                        <input id="url" name="url" type="url"
                                               placeholder="http://scep.example.com/scep" required />
                                    </Form.Field>


                                    <Form.Field>
                                        <small className="float-right">Optional. Any string that is understood by the SCEP server.</small>
                                        <label>Name</label>
                                        <input id="name" name="name" type="text" placeholder="CA-NAME or organization.org"/>
                                    </Form.Field>

                                    <Form.Field>
                                        <label>Challenge</label>
                                        <input id="challenge" name="challenge" type="password" />
                                    </Form.Field>
                                    <small className="float-right">Optional. Used as the pre-shared secret for automatic enrollment
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
                        <input type="text" id="subject" name="subject" placeholder="O=Commandment/OU=IT/CN=%HardwareUUID%" />
                    </Form.Field>
                    <Header size='tiny'>Key size (in bits)</Header>

                    <Form.Field>
                        <Radio label="1024 bits"
                               name="key_size"
                               value="1024"
                               checked={this.state.key_size == '1024'}
                               onChange={this.handleChangeKeySize}
                        />
                    </Form.Field>
                    <Form.Field>
                        <Radio label="2048 bits"
                               name="key_size"
                               value="2048"
                               checked={this.state.key_size == '2048'}
                               onChange={this.handleChangeKeySize}
                        />
                    </Form.Field>

                    <Header size='tiny'>Use SCEP key for</Header>
                    <Form.Field>
                        <Checkbox label="Signing" value="1" />
                    </Form.Field>
                    <Form.Field>
                        <Checkbox label="Encryption" value="4" />
                    </Form.Field>

                    <Form.Field>
                        <label>Retries</label>
                        <input type="number" id="retries" name="retries" value={this.state.retries}
                               onChange={(event: React.FormEvent<HTMLInputElement>) =>
                                   this.setState({ retries: parseInt(event.currentTarget.value, 0) })} />
                        <p>The number of times the device should retry if the server sends a PENDING response</p>
                    </Form.Field>

                    <Form.Field>
                        <label>Retry Delay</label>
                        <input type="number" id="retry_delay" name="retry_delay" value={this.state.retry_delay}
                               onChange={(event: React.FormEvent<HTMLInputElement>) =>
                                   this.setState({ retry_delay: parseInt(event.currentTarget.value, 0) })} />
                        <p>The number of seconds to wait between subsequent retries. The first retry is attempted without
                            this delay</p>
                    </Form.Field>
                    {/*<Message*/}
                        {/*success*/}
                        {/*header="Form Completed"*/}
                        {/*content="SCEP details saved"*/}
                    {/*/>*/}

                    {/*<Form.Group>*/}
                        {/*<Form.Button type="button" disabled={pristine || submitting} onClick={reset}>*/}
                            {/*Revert*/}
                        {/*</Form.Button>*/}
                        {/*<Form.Button type="submit" primary disabled={pristine || submitting}>Save</Form.Button>*/}
                    {/*</Form.Group>*/}
                </Segment>
            </Form>
        )
    }
}
