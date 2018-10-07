import * as React from "react";
import Form from "semantic-ui-react/dist/commonjs/collections/Form/Form";
import Checkbox from "semantic-ui-react/dist/commonjs/collections/Form/FormCheckbox";
import Segment from "semantic-ui-react/dist/commonjs/elements/Segment/Segment";
import Header from "semantic-ui-react/dist/commonjs/elements/Header/Header";



export class DEPProfileForm extends React.Component {
    render() {
        return (
            <Form>
                <Form.Field>
                    <label>Profile Name</label>
                    <input type='text' />
                </Form.Field>
                <Form.Field>
                    <label>MDM URL</label>
                    <input type='text' />
                </Form.Field>
                <Form.Field>
                    <Checkbox toggle label='Allow Pairing' />
                </Form.Field>
                <Form.Field>
                    <Checkbox toggle label='Supervised' />
                </Form.Field>
                <Form.Field>
                    <Checkbox toggle label='Shared iPad' />
                </Form.Field>
                <Form.Field>
                    <Checkbox toggle label='Mandatory' />
                </Form.Field>
                <Form.Field>
                    <Checkbox toggle label='Await Configured' />
                </Form.Field>
                <Form.Field>
                    <Checkbox toggle label='MDM Payload Removable' />
                </Form.Field>
                <Form.Field>
                    <label>Support Phone Number</label>
                    <input type='text' />
                </Form.Field>
                <Form.Field>
                    <Checkbox label='Auto Advance (tvOS)' />
                </Form.Field>
                <Form.Field>
                    <label>Support E-mail Address</label>
                    <input type='email' />
                </Form.Field>
                <Segment>
                    <Header>Setup Assistant Steps</Header>

                    <Form.Field>
                        <Checkbox toggle label='Skip Apple ID Setup' />
                    </Form.Field>
                    <Form.Field>
                        <Checkbox toggle label='Skip Touch ID' />
                    </Form.Field>
                    <Form.Field>
                        <Checkbox toggle label='Skip Diagnostics' />
                    </Form.Field>
                    <Form.Field>
                        <Checkbox toggle label='Skip DisplayTone' />
                    </Form.Field>
                    <Form.Field>
                        <Checkbox toggle label='Skip Location Services' />
                    </Form.Field>
                    <Form.Field>
                        <Checkbox toggle label='Skip Passcode Setup' />
                    </Form.Field>
                    <Form.Field>
                        <Checkbox toggle label='Skip Apple Pay' />
                    </Form.Field>
                    <Form.Field>
                        <Checkbox toggle label='Skip Privacy' />
                    </Form.Field>
                    <Form.Field>
                        <Checkbox toggle label='Skip Restore from Backup' />
                    </Form.Field>
                    <Form.Field>
                        <Checkbox toggle label='Skip Add Cellular Plan' />
                    </Form.Field>
                    <Form.Field>
                        <Checkbox toggle label='Skip Siri' />
                    </Form.Field>
                    <Form.Field>
                        <Checkbox toggle label='Skip Terms and Conditions' />
                    </Form.Field>
                    <Form.Field>
                        <Checkbox toggle label='Skip Zoom' />
                    </Form.Field>
                    <Form.Field>
                        <Checkbox toggle label='Disable Restore from Android' />
                    </Form.Field>
                    <Form.Field>
                        <Checkbox toggle label='Skip Home Button Sensitivity' />
                    </Form.Field>
                    <Form.Field>
                        <Checkbox toggle label='Skip iMessage and FaceTime' />
                    </Form.Field>
                    <Form.Field>
                        <Checkbox toggle label='Skip On-Boarding' />
                    </Form.Field>
                    <Form.Field>
                        <Checkbox toggle label='Skip Screen Time' />
                    </Form.Field>
                    <Form.Field>
                        <Checkbox toggle label='Skip Mandatory Software Update Screen' />
                    </Form.Field>
                    <Form.Field>
                        <Checkbox toggle label='Skip Watch Migration' />
                    </Form.Field>
                    <Form.Field>
                        <Checkbox toggle label='Skip Choose your Look' />
                    </Form.Field>
                </Segment>
            </Form>
        )
    }
}
