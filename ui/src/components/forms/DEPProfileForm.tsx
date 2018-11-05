import {Formik} from "formik";
import * as React from "react";
import {ChangeEvent, FormEvent} from "react";
import {AccordionTitleProps, CheckboxProps} from "semantic-ui-react";
import Form, {FormProps} from "semantic-ui-react/dist/commonjs/collections/Form/Form";
import Checkbox from "semantic-ui-react/dist/commonjs/collections/Form/FormCheckbox";
import Button from "semantic-ui-react/dist/commonjs/elements/Button/Button";
import Divider from "semantic-ui-react/dist/commonjs/elements/Divider/Divider";
import Header from "semantic-ui-react/dist/commonjs/elements/Header/Header";
import Icon from "semantic-ui-react/dist/commonjs/elements/Icon/Icon";
import Segment from "semantic-ui-react/dist/commonjs/elements/Segment/Segment";
import Accordion from "semantic-ui-react/dist/commonjs/modules/Accordion/Accordion";
import Dropdown from "semantic-ui-react/dist/commonjs/modules/Dropdown/Dropdown";
import {DEPProfile, SkipSetupSteps} from "../../store/dep/types";
import * as Yup from "yup";
import {FormikCheckbox} from "../formik/FormikCheckbox";
import Label from "semantic-ui-react/dist/commonjs/elements/Label/Label";

export interface IDEPProfileFormValues extends DEPProfile {
    show: { [SkipSetupSteps: string]: boolean };
}

export interface IDEPProfileFormProps {
    data?: DEPProfile;
    onSubmit: (data: DEPProfile) => void;
}

export interface IDEPProfileFormState {
    activeIndex: number;
}

export enum DEPProfilePairWithOptions {
    AnyComputer = "AnyComputer",
    Certificates = "Certificates",
}

const initialValues: IDEPProfileFormValues = {
    profile_name: "",
    allow_pairing: true,
    is_supervised: true,
    show: {
        [SkipSetupSteps.AppleID]: true,
        [SkipSetupSteps.Biometric]: true,
        [SkipSetupSteps.Diagnostics]: true,
        [SkipSetupSteps.DisplayTone]: true,
        [SkipSetupSteps.Location]: true,
        [SkipSetupSteps.Passcode]: true,
        [SkipSetupSteps.Payment]: true,
        [SkipSetupSteps.Privacy]: true,
        [SkipSetupSteps.Restore]: true,
        [SkipSetupSteps.SIMSetup]: true,
        [SkipSetupSteps.Siri]: true,
        [SkipSetupSteps.TOS]: true,
        [SkipSetupSteps.Zoom]: true,
        [SkipSetupSteps.Android]: true,
        [SkipSetupSteps.HomeButtonSensitivity]: true,
        [SkipSetupSteps.iMessageAndFaceTime]: true,
        [SkipSetupSteps.OnBoarding]: true,
        [SkipSetupSteps.ScreenTime]: true,
        [SkipSetupSteps.SoftwareUpdate]: true,
        [SkipSetupSteps.WatchMigration]: true,
        [SkipSetupSteps.Appearance]: true,
        [SkipSetupSteps.FileVault]: true,
        [SkipSetupSteps.iCloudDiagnostics]: true,
        [SkipSetupSteps.iCloudStorage]: true,
        [SkipSetupSteps.Registration]: true,
        [SkipSetupSteps.ScreenSaver]: true,
        [SkipSetupSteps.TapToSetup]: true,
        [SkipSetupSteps.TVHomeScreenSync]: true,
        [SkipSetupSteps.TVProviderSignIn]: true,
        [SkipSetupSteps.TVRoom]: true,
    },
};

export class DEPProfileForm extends React.Component<IDEPProfileFormProps, IDEPProfileFormState> {

    constructor(props: IDEPProfileFormProps) {
        super(props);
        this.state = {
            activeIndex: 0,
        };
    }

    handleClick = (evt: MouseEvent, data: AccordionTitleProps) => {
        this.setState({activeIndex: parseInt(data.index, 0)});
    };

    handleSubmit = (event: React.FormEvent<HTMLFormElement>, data: FormProps) => {
        this.props.onSubmit(this.state.formValues);
    };

    public render() {
        const activeIndex = this.state.activeIndex;
        return (
            <Formik
                initialValues={initialValues}
                onSubmit={(values: IDEPProfileFormValues) => this.handleSubmit}
                validationSchema={Yup.object().shape({
                    profile_name: Yup.string().required('Required'),
                })}
            >
                {({
                      values,
                      errors,
                      touched,
                      handleChange,
                      handleBlur,
                      handleSubmit,
                      isSubmitting,
                  }) => (
                    <Form onSubmit={handleSubmit}>
                        <Accordion fluid styled>
                            <Accordion.Title active={activeIndex == 0} index={0} onClick={this.handleClick}>
                                <Icon name="dropdown"/>
                                General
                            </Accordion.Title>
                            <Accordion.Content active={activeIndex === 0}>
                                <Form.Field required>
                                    <label>Profile Name</label>
                                    <input type="text" name="profile_name"
                                           onChange={handleChange} onBlur={handleBlur}
                                           value={values.profile_name}/>
                                    {errors.profile_name && touched.profile_name && <Label pointing>{errors.profile_name}</Label>}
                                </Form.Field>

                                <Form.Field>
                                    <label>Support Phone Number</label>
                                    <input type="tel" name="support_phone_number"
                                           onChange={handleChange} onBlur={handleBlur}
                                           value={values.support_phone_number}/>
                                    {errors.support_phone_number &&
                                    touched.support_phone_number &&
                                    errors.support_phone_number}
                                </Form.Field>
                                <Form.Field>
                                    <label>Support E-mail Address</label>
                                    <input type="email" name="support_email_address"
                                           onChange={handleChange} onBlur={handleBlur}
                                           value={values.support_email_address}/>
                                    {errors.support_email_address &&
                                    touched.support_email_address &&
                                    errors.support_email_address}
                                </Form.Field>

                                <FormikCheckbox toggle name="allow_pairing" label="Allow Pairing"/>
                                <FormikCheckbox toggle name="is_supervised"
                                                label="Supervised (will be required in a future version of iOS)"
                                                defaultChecked/>
                                <FormikCheckbox toggle name="is_multi_user" label="Shared iPad" />
                                <FormikCheckbox toggle name="is_mandatory"
                                                label="Mandatory. User cannot skip Remote Management" />
                                <FormikCheckbox toggle name="await_device_configured" label="Await Configured" />
                                <FormikCheckbox toggle name="is_mdm_removable" label="MDM Payload Removable" />
                                <FormikCheckbox toggle name="auto_advance_setup" label="Auto Advance (tvOS)" />
                            </Accordion.Content>

                            <Accordion.Title active={activeIndex == 1} index={1} onClick={this.handleClick}>
                                <Icon name="dropdown"/>
                                Setup Assistant Steps (Common)
                            </Accordion.Title>
                            <Accordion.Content active={activeIndex === 1}>
                                <FormikCheckbox toggle name={`show.${SkipSetupSteps.AppleID}`}
                                                label="Show Apple ID Setup"
                                                value={SkipSetupSteps.AppleID}/>
                                <FormikCheckbox toggle name={`show.${SkipSetupSteps.Biometric}`} label="Show Touch ID"
                                                value={SkipSetupSteps.Biometric}/>
                                <FormikCheckbox toggle name={`show.${SkipSetupSteps.Diagnostics}`}
                                                label="Show Diagnostics"
                                                value={SkipSetupSteps.Diagnostics}/>
                                <FormikCheckbox toggle name={`show.${SkipSetupSteps.DisplayTone}`}
                                                label="Show DisplayTone"
                                                value={SkipSetupSteps.DisplayTone}/>
                                <FormikCheckbox toggle name={`show.${SkipSetupSteps.Location}`}
                                                label="Show Location Services"
                                                value={SkipSetupSteps.Location}/>
                                <FormikCheckbox toggle name={`show.${SkipSetupSteps.Passcode}`}
                                                label="Show Passcode Setup"
                                                value={SkipSetupSteps.Passcode}/>
                                <FormikCheckbox toggle name={`show.${SkipSetupSteps.Payment}`} label="Show Apple Pay"
                                                value={SkipSetupSteps.Payment}/>
                                <FormikCheckbox toggle name={`show.${SkipSetupSteps.Privacy}`} label="Show Privacy"
                                                value={SkipSetupSteps.Privacy}/>
                                <FormikCheckbox toggle name={`show.${SkipSetupSteps.Restore}`}
                                                label="Show Restore from Backup"
                                                value={SkipSetupSteps.Restore}/>
                                <FormikCheckbox toggle name={`show.${SkipSetupSteps.SIMSetup}`}
                                                label="Show Add Cellular Plan"
                                                value={SkipSetupSteps.SIMSetup}/>
                                <FormikCheckbox toggle name={`show.${SkipSetupSteps.Siri}`} label="Show Siri"
                                                value={SkipSetupSteps.Siri}/>
                                <FormikCheckbox toggle name={`show.${SkipSetupSteps.TOS}`}
                                                label="Show Terms and Conditions"
                                                value={SkipSetupSteps.TOS}/>
                                <FormikCheckbox toggle name={`show.${SkipSetupSteps.Zoom}`} label="Show Zoom"
                                                value={SkipSetupSteps.Zoom}/>
                            </Accordion.Content>
                            <Accordion.Title active={activeIndex == 2} index={2} onClick={this.handleClick}>
                                <Icon name="dropdown" />
                                Setup Assistant Steps (iOS)
                            </Accordion.Title>
                            <Accordion.Content active={activeIndex === 2}>
                                <FormikCheckbox toggle name={`show.${SkipSetupSteps.Android}`}
                                                label="Show Restore from Android"
                                                value={SkipSetupSteps.Android} />
                                <FormikCheckbox toggle name={`show.${SkipSetupSteps.HomeButtonSensitivity}`}
                                                label="Show Home Button Sensitivity"
                                                value={SkipSetupSteps.HomeButtonSensitivity} />
                                <FormikCheckbox toggle name={`show.${SkipSetupSteps.iMessageAndFaceTime}`}
                                                label="Show iMessage and FaceTime"
                                                value={SkipSetupSteps.iMessageAndFaceTime} />
                                <FormikCheckbox toggle name={`show.${SkipSetupSteps.OnBoarding}`}
                                                label="Show On-Boarding"
                                                value={SkipSetupSteps.OnBoarding}/>
                                <FormikCheckbox toggle name={`show.${SkipSetupSteps.ScreenTime}`}
                                                label="Show Screen Time"
                                                value={SkipSetupSteps.ScreenTime}/>
                                <FormikCheckbox toggle name={`show.${SkipSetupSteps.SoftwareUpdate}`}
                                                label="Show Mandatory Software Update Screen"
                                                value={SkipSetupSteps.SoftwareUpdate}/>
                                <FormikCheckbox toggle name={`show.${SkipSetupSteps.WatchMigration}`}
                                                label="Show Watch Migration"
                                                value={SkipSetupSteps.WatchMigration} />
                            </Accordion.Content>
                          <Accordion.Title active={activeIndex == 3} index={3} onClick={this.handleClick}>
                            <Icon name="dropdown" />
                            Setup Assistant Steps (macOS)
                          </Accordion.Title>
                            <Accordion.Content active={activeIndex === 3}>
                                <FormikCheckbox toggle name={`show.${SkipSetupSteps.Appearance}`}
                                                label="Show Choose your Look"
                                                value={SkipSetupSteps.Appearance} />
                                <FormikCheckbox toggle name={`show.${SkipSetupSteps.FileVault}`}
                                                label="Show FileVault on macOS"
                                                value={SkipSetupSteps.FileVault} />
                                <FormikCheckbox toggle name={`show.${SkipSetupSteps.iCloudDiagnostics}`}
                                                label="Show iCloud Analytics"
                                                value={SkipSetupSteps.iCloudDiagnostics} />
                                <FormikCheckbox toggle name={`show.${SkipSetupSteps.iCloudStorage}`}
                                                label="Show iCloud Desktop and Documents"
                                                value={SkipSetupSteps.iCloudStorage} />
                                <FormikCheckbox toggle name={`show.${SkipSetupSteps.Registration}`}
                                                label="Show Registration"
                                                value={SkipSetupSteps.Registration} />
                            </Accordion.Content>
                          <Accordion.Title active={activeIndex == 4} index={4} onClick={this.handleClick}>
                            <Icon name="dropdown" />
                            Setup Assistant Steps (tvOS)
                          </Accordion.Title>
                            <Accordion.Content active={activeIndex === 4}>
                                <FormikCheckbox toggle name={`show.${SkipSetupSteps.ScreenSaver}`}
                                                label="Show Screen about using Aerial Screensavers in ATV"
                                                value={SkipSetupSteps.ScreenSaver}/>
                                <FormikCheckbox toggle name={`show.${SkipSetupSteps.TapToSetup}`}
                                                label="Show Tap to Set Up option in ATV which uses an iOS device to set up"
                                                value={SkipSetupSteps.TapToSetup}/>
                                <FormikCheckbox toggle name={`show.${SkipSetupSteps.TVHomeScreenSync}`}
                                                label="Show home screen layout sync"
                                                value={SkipSetupSteps.TVHomeScreenSync}/>
                                <FormikCheckbox toggle name={`show.${SkipSetupSteps.TVProviderSignIn}`}
                                                label="Show TV provider sign in"
                                                value={SkipSetupSteps.TVProviderSignIn}/>
                                <FormikCheckbox toggle name={`show.${SkipSetupSteps.TVRoom}`}
                                                label='Show "Where is this Apple TV?" screen'
                                                value={SkipSetupSteps.TVRoom}/>
                            </Accordion.Content>
                        </Accordion>
                        <Divider hidden/>
                        <Button type="submit" disabled={isSubmitting}>Submit</Button>
                    </Form>
                )}
            </Formik>
        );
    }
}
