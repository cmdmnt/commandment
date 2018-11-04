import * as React from "react";
import Form, {FormProps} from "semantic-ui-react/dist/commonjs/collections/Form/Form";
import Checkbox from "semantic-ui-react/dist/commonjs/collections/Form/FormCheckbox";
import Segment from "semantic-ui-react/dist/commonjs/elements/Segment/Segment";
import Header from "semantic-ui-react/dist/commonjs/elements/Header/Header";
import Accordion from "semantic-ui-react/dist/commonjs/modules/Accordion/Accordion";
import Icon from "semantic-ui-react/dist/commonjs/elements/Icon/Icon";
import {AccordionTitleProps, CheckboxProps} from "semantic-ui-react";
import {DEPProfile, SkipSetupSteps} from "../../store/dep/types";
import Divider from "semantic-ui-react/dist/commonjs/elements/Divider/Divider";
import Dropdown from "semantic-ui-react/dist/commonjs/modules/Dropdown/Dropdown";
import Button from "semantic-ui-react/dist/commonjs/elements/Button/Button";
import {ChangeEvent, FormEvent} from "react";

export interface IDEPProfileFormProps {
    data?: DEPProfile;
    onSubmit: (data: DEPProfile) => void;
}

export interface IDEPProfileFormState {
    activeIndex: number;
    formValues: DEPProfile;
}

export enum DEPProfilePairWithOptions {
    AnyComputer = "AnyComputer",
    Certificates = "Certificates"
}

const defaultProps = {

};

export class DEPProfileForm extends React.Component<IDEPProfileFormProps, IDEPProfileFormState> {

    constructor(props: IDEPProfileFormProps) {
        super(props);
        this.state = {
            activeIndex: 0,
            formValues: {
                skip_setup_items: []
            },
        };
    }

    handleClick = (evt: MouseEvent, data: AccordionTitleProps) => {
        this.setState({ activeIndex: parseInt(data.index, 0) });
    };

    handleFormChange = (evt: ChangeEvent<HTMLInputElement>) => {
        const update = {
            ...this.state.formValues,
            [evt.target.name]: evt.target.value
        };

        this.setState({
            formValues: update
        });
    };

    handleCheckboxChange = (evt: ChangeEvent<HTMLInputElement>, data: CheckboxProps) => {
        console.log(data);

        const update = {
            ...this.state.formValues,
            [data.name]: data.checked
        };

        this.setState({
            formValues: update
        });
    };

    handleCheckboxArrayChange = (evt: ChangeEvent<HTMLInputElement>, data: CheckboxProps) => {
        console.log(data);

        const oldSelection: string[] = this.state.formValues['skip_setup_items'];
        let newSelection: string[] = [];
        if (data.checked && oldSelection.indexOf(data.value) == -1) {
            newSelection = [...oldSelection, data.value];
        } else if (!data.checked && oldSelection.indexOf(data.value) > -1) {
            newSelection = oldSelection.splice(oldSelection.indexOf(data.value), 1);
        } else {
            console.log("This could be a bug");
            newSelection = oldSelection;
        }

        const update = {
            ...this.state.formValues,
            ['skip_setup_items']: newSelection
        };

        this.setState({
            formValues: update
        });
    };

    handleSubmit = (event: React.FormEvent<HTMLFormElement>, data: FormProps) => {
        this.props.onSubmit(this.state.formValues);
    };

    render() {
        const activeIndex = this.state.activeIndex;
        return (
            <Form onSubmit={this.handleSubmit}>
                <Accordion fluid styled>
                    <Accordion.Title active={activeIndex == 0} index={0} onClick={this.handleClick}>
                        <Icon name='dropdown' />
                        General
                    </Accordion.Title>
                    <Accordion.Content active={activeIndex == 0}>
                        <Form.Field required>
                            <label>Profile Name</label>
                            <input type='text' name='profile_name' onChange={this.handleFormChange} value={this.state.formValues.profile_name} />
                        </Form.Field>

                        <Form.Field>
                            <label>Support Phone Number</label>
                            <input type='text' name='support_phone_number' onChange={this.handleFormChange} value={this.state.formValues.support_phone_number} />
                        </Form.Field>
                        <Form.Field>
                            <label>Support E-mail Address</label>
                            <input type='email' name='support_email_address' onChange={this.handleFormChange} value={this.state.formValues.support_email_address} />
                        </Form.Field>
                        {/*<Form.Field>*/}
                            {/*<label>MDM URL</label>*/}
                            {/*<input type='text' />*/}
                        {/*</Form.Field>*/}
                        <Form.Field>
                            <Checkbox toggle name='allow_pairing' label='Allow Pairing' onChange={this.handleCheckboxChange} value="true" checked={this.state.formValues.allow_pairing == true} />
                        </Form.Field>
                        <Form.Field>
                            <Checkbox toggle name='is_supervised' label='Supervised (will be required in a future version of iOS)' onChange={this.handleCheckboxChange} defaultChecked />
                        </Form.Field>
                        <Form.Field>
                            <Checkbox toggle name='is_multi_user' label='Shared iPad' onChange={this.handleCheckboxChange} />
                        </Form.Field>
                        <Form.Field>
                            <Checkbox toggle name='is_mandatory' label='Mandatory. User cannot skip Remote Management' onChange={this.handleCheckboxChange} />
                        </Form.Field>
                        <Form.Field>
                            <Checkbox toggle name='await_device_configured' label='Await Configured' onChange={this.handleCheckboxChange} />
                        </Form.Field>
                        <Form.Field>
                            <Checkbox toggle name='is_mdm_removable' label='MDM Payload Removable' onChange={this.handleCheckboxChange} />
                        </Form.Field>
                        <Form.Field>
                            <Checkbox toggle name='auto_advance_setup' label='Auto Advance (tvOS)' onChange={this.handleCheckboxChange} />
                        </Form.Field>

                    </Accordion.Content>

                    <Accordion.Title active={activeIndex == 1} index={1} onClick={this.handleClick}>
                        <Icon name='dropdown' />
                        Setup Assistant Steps
                    </Accordion.Title>
                    <Accordion.Content active={activeIndex == 1}>
                        <Header as="h5">Multiple Platforms</Header>
                        <Form.Field>
                            <Checkbox toggle name='skip_setup_items[]' label='Show Apple ID Setup' value={SkipSetupSteps.AppleID} onChange={this.handleCheckboxArrayChange} checked={this.state.formValues.skip_setup_items.indexOf(SkipSetupSteps.AppleID) == -1} />
                        </Form.Field>
                        <Form.Field>
                            <Checkbox toggle name='skip_setup_items[]' label='Show Touch ID' defaultChecked value={SkipSetupSteps.Biometric} onChange={this.handleCheckboxArrayChange} />
                        </Form.Field>
                        <Form.Field>
                            <Checkbox toggle name='skip_setup_items[]' label='Show Diagnostics' defaultChecked value={SkipSetupSteps.Diagnostics} onChange={this.handleCheckboxArrayChange} />
                        </Form.Field>
                        <Form.Field>
                            <Checkbox toggle name='skip_setup_items[]' label='Show DisplayTone' defaultChecked value={SkipSetupSteps.DisplayTone} onChange={this.handleCheckboxArrayChange} />
                        </Form.Field>
                        <Form.Field>
                            <Checkbox toggle name='skip_setup_items[]' label='Show Location Services' defaultChecked value={SkipSetupSteps.Location} onChange={this.handleCheckboxArrayChange} />
                        </Form.Field>
                        <Form.Field>
                            <Checkbox toggle name='skip_setup_items[]' label='Show Passcode Setup' defaultChecked value={SkipSetupSteps.Passcode} onChange={this.handleCheckboxChange} />
                        </Form.Field>
                        <Form.Field>
                            <Checkbox toggle name='skip_setup_items[]' label='Show Apple Pay' defaultChecked value={SkipSetupSteps.Payment} onChange={this.handleCheckboxChange} />
                        </Form.Field>
                        <Form.Field>
                            <Checkbox toggle name='skip_setup_items[]' label='Show Privacy' defaultChecked value={SkipSetupSteps.Privacy} onChange={this.handleCheckboxChange} />
                        </Form.Field>
                        <Form.Field>
                            <Checkbox toggle name='skip_setup_items[]' label='Show Restore from Backup' defaultChecked value={SkipSetupSteps.Restore} onChange={this.handleCheckboxChange} />
                        </Form.Field>
                        <Form.Field>
                            <Checkbox toggle name='skip_setup_items[]' label='Show Add Cellular Plan' defaultChecked value={SkipSetupSteps.SIMSetup} onChange={this.handleCheckboxChange} />
                        </Form.Field>
                        <Form.Field>
                            <Checkbox toggle name='skip_setup_items[]' label='Show Siri' defaultChecked value={SkipSetupSteps.Siri} onChange={this.handleCheckboxChange} />
                        </Form.Field>
                        <Form.Field>
                            <Checkbox toggle name='skip_setup_items[]' label='Show Terms and Conditions' defaultChecked value={SkipSetupSteps.TOS} onChange={this.handleCheckboxChange} />
                        </Form.Field>
                        <Form.Field>
                            <Checkbox toggle name='skip_setup_items[]' label='Show Zoom' defaultChecked value={SkipSetupSteps.Zoom} onChange={this.handleCheckboxChange} />
                        </Form.Field>


                        <Divider />
                        <Header as="h5">iOS</Header>
                        <Form.Field>
                            <Checkbox toggle name='skip_setup_items[]' label='Show Restore from Android' defaultChecked value={SkipSetupSteps.Android} />
                        </Form.Field>
                        <Form.Field>
                            <Checkbox toggle name='skip_setup_items[]' label='Show Home Button Sensitivity' defaultChecked value={SkipSetupSteps.HomeButtonSensitivity} />
                        </Form.Field>
                        <Form.Field>
                            <Checkbox toggle name='skip_setup_items[]' label='Show iMessage and FaceTime' defaultChecked value={SkipSetupSteps.iMessageAndFaceTime} />
                        </Form.Field>
                        <Form.Field>
                            <Checkbox toggle name='skip_setup_items[]' label='Show On-Boarding' defaultChecked value={SkipSetupSteps.OnBoarding} />
                        </Form.Field>
                        <Form.Field>
                            <Checkbox toggle name='skip_setup_items[]' label='Show Screen Time' defaultChecked value={SkipSetupSteps.ScreenTime} />
                        </Form.Field>
                        <Form.Field>
                            <Checkbox toggle name='skip_setup_items[]' label='Show Mandatory Software Update Screen' defaultChecked value={SkipSetupSteps.SoftwareUpdate} />
                        </Form.Field>
                        <Form.Field>
                            <Checkbox toggle name='skip_setup_items[]' label='Show Watch Migration' defaultChecked value={SkipSetupSteps.WatchMigration} />
                        </Form.Field>

                        <Divider />
                        <Header as="h5">macOS</Header>
                        <Form.Field>
                            <Checkbox toggle name='skip_setup_items[]' label='Show Choose your Look' defaultChecked value={SkipSetupSteps.Appearance} />
                        </Form.Field>
                        <Form.Field>
                            <Checkbox toggle name='skip_setup_items[]' label='Show FileVault on macOS' defaultChecked value={SkipSetupSteps.FileVault} />
                        </Form.Field>
                        <Form.Field>
                            <Checkbox toggle name='skip_setup_items[]' label='Show iCloud Analytics' defaultChecked value={SkipSetupSteps.iCloudDiagnostics} />
                        </Form.Field>
                        <Form.Field>
                            <Checkbox toggle name='skip_setup_items[]' label='Show iCloud Desktop and Documents' defaultChecked value={SkipSetupSteps.iCloudStorage} />
                        </Form.Field>
                        <Form.Field>
                            <Checkbox toggle name='skip_setup_items[]' label='Show Registration' defaultChecked value={SkipSetupSteps.Registration} />
                        </Form.Field>

                        <Divider />
                        <Header as="h5">tvOS</Header>
                        <Form.Field>
                            <Checkbox toggle name='skip_setup_items[]' label='Show Screen about using Aerial Screensavers in ATV' defaultChecked value={SkipSetupSteps.ScreenSaver} />
                        </Form.Field>
                        <Form.Field>
                            <Checkbox toggle name='skip_setup_items[]' label='Show Tap to Set Up option in ATV which uses an iOS device to set up' defaultChecked value={SkipSetupSteps.TapToSetup} />
                        </Form.Field>
                        <Form.Field>
                            <Checkbox toggle name='skip_setup_items[]' label='Show home screen layout sync' defaultChecked value={SkipSetupSteps.TVHomeScreenSync} />
                        </Form.Field>
                        <Form.Field>
                            <Checkbox toggle name='skip_setup_items[]' label='Show TV provider sign in' defaultChecked value={SkipSetupSteps.TVProviderSignIn} />
                        </Form.Field>
                        <Form.Field>
                            <Checkbox toggle name='skip_setup_items[]' label='Show "Where is this Apple TV?" screen' defaultChecked value={SkipSetupSteps.TVRoom} />
                        </Form.Field>
                    </Accordion.Content>
                </Accordion>
                <Divider hidden />
                <Button type='submit'>Submit</Button>
            </Form>
        )
    }
}
