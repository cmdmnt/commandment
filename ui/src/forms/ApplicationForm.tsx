import * as React from "react";
import {Field, FormProps, reduxForm} from "redux-form";
import Form from "semantic-ui-react/src/collections/Form";
import Button from "semantic-ui-react/src/elements/Button";
import Grid from "semantic-ui-react/src/collections/Grid";
import Header from "semantic-ui-react/src/elements/Header";
import Icon from "semantic-ui-react/src/elements/Icon";
import Input from "semantic-ui-react/src/elements/Input";
import Message from "semantic-ui-react/src/collections/Message";
import Segment from "semantic-ui-react/src/elements/Segment";

import {Application} from "../models";
import {SemanticInput} from "./fields/SemanticInput";
import {SemanticTextArea} from "./fields/SemanticTextArea";

export interface FormData extends Application {

}

interface ApplicationFormProps extends FormProps<FormData, any, any> {

}

const UnconnectedApplicationForm: React.StatelessComponent<ApplicationFormProps> = (props) => {
        const { error, handleSubmit, pristine, reset, submitting } = props;

        return (
            <Form onSubmit={handleSubmit} error={error}>
                <Message attached>Enterprise Application (.pkg)</Message>
                <Segment attached>
                    <Form.Group>
                        <Field
                            id="display-name"
                            label="Display Name"
                            name="display_name"
                            component={SemanticInput}
                            width={12}
                            type="text" required />
                        <Field
                            id="version"
                            label="Version"
                            name="version"
                            width={4}
                            component={SemanticInput}
                            type="text" required />
                    </Form.Group>
                    <Field
                        id="description"
                        label="Description"
                        name="description"
                        component={SemanticTextArea}
                        type="TextArea" />
                    <Field
                        id="manifest-url"
                        label="Manifest URL"
                        name="manifest_url"
                        component={SemanticInput}
                        type="text" />
                    <Field
                        id="management-flags-remove-app"
                        label="Remove application when MDM profile is removed"
                        name="management_flags_remove_app"
                        component={SemanticInput}
                        type="checkbox" />
                    <Field
                        id="management-flags-prevent-backup"
                        label="Prevent backup of application data"
                        name="management_flags_prevent_backup"
                        component={SemanticInput}
                        type="checkbox" />
                    <Button type="submit" disabled={submitting}>Save</Button>
                </Segment>
            </Form>
        );
};

export const ApplicationForm = reduxForm<FormData, ApplicationFormProps, undefined>({
    form: "application",
})(UnconnectedApplicationForm);
