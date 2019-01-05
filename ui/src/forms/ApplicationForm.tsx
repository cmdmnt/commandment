import * as React from "react";
// import {Field, FormProps, reduxForm} from "redux-form";
// import Form from "semantic-ui-react/src/collections/Form";
// import Message from "semantic-ui-react/src/collections/Message";
// import Button from "semantic-ui-react/src/elements/Button";
// import Segment from "semantic-ui-react/src/elements/Segment";
//
// import Icon from "semantic-ui-react/dist/commonjs/elements/Icon/Icon";
import {Application} from "../store/applications/types";
// import {SemanticCheckbox} from "./fields/SemanticCheckbox";
// import {SemanticInput} from "./fields/SemanticInput";
// import {SemanticTextArea} from "./fields/SemanticTextArea";
// import {httpsURL} from "../validations";
//
export interface IFormData extends Application {

}
//
// interface IApplicationFormProps extends FormProps<IFormData, any, any> {
//     onClickFetch: (e: any) => void;
// }
//
// const UnconnectedApplicationForm: React.StatelessComponent<IApplicationFormProps> = (props) => {
//         const { error, handleSubmit, pristine, reset, submitting } = props;
//
//         return (
//             <Form onSubmit={handleSubmit} error={error}>
//                 <Message attached>Enterprise Application (.pkg)</Message>
//                 <Segment attached>
//                     <Field
//                         id="manifest-url"
//                         label="Manifest URL"
//                         name="manifest_url"
//                         component={SemanticInput}
//                         type="text"
//                         validate={[httpsURL]}
//                         action={<Button icon labelPosition="right" onClick={this.onClickFetch}>
//                             <Icon name="cloud download" /> Fetch</Button>}
//                     />
//                 </Segment>
//                 <Segment attached>
//                     <Form.Group>
//                         <Field
//                             id="display-name"
//                             label="Display Name"
//                             name="display_name"
//                             component={SemanticInput}
//                             width={12}
//                             type="text" required />
//                         <Field
//                             id="version"
//                             label="Version"
//                             name="version"
//                             width={4}
//                             component={SemanticInput}
//                             type="text" required />
//                     </Form.Group>
//                     {/*<Field*/}
//                         {/*id="itunes-store-id"*/}
//                         {/*label="iTunes store ID"*/}
//                         {/*name="itunes_store_id"*/}
//                         {/*component={SemanticInput}*/}
//                         {/*type="text" />*/}
//                     <Field
//                         id="bundle-id"
//                         label="Bundle Identifier"
//                         name="bundle_id"
//                         component={SemanticInput}
//                         type="text" />
//                     <Field
//                         id="description"
//                         label="Description"
//                         name="description"
//                         component={SemanticTextArea}
//                         type="TextArea" />
//                 </Segment>
//                 <Message attached>Management Options</Message>
//                 <Segment attached>
//                     <Field
//                         id="management-flags-remove-app"
//                         label="Remove application when MDM profile is removed"
//                         name="management_flags_remove_app"
//                         component={SemanticCheckbox}
//                         type="checkbox" />
//                     <Field
//                         id="management-flags-prevent-backup"
//                         label="App data cannot be backed up to iCloud or iTunes"
//                         name="management_flags_prevent_backup"
//                         component={SemanticCheckbox}
//                         type="checkbox" />
//                     <Field
//                         id="change-management-state"
//                         label="Take management of this application if it is already installed"
//                         name="change_management_state"
//                         component={SemanticCheckbox}
//                         type="checkbox"
//                         value="Managed" />
//                     <Button type="submit" disabled={submitting}>Save</Button>
//                 </Segment>
//             </Form>
//         );
// };
//
// export const ApplicationForm = reduxForm<IFormData, IApplicationFormProps, undefined>({
//     form: "application",
// })(UnconnectedApplicationForm);
