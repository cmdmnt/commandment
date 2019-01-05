import * as React from "react";
import Dropzone, {DropFilesEventHandler} from "react-dropzone";
import {RouteComponentProps} from "react-router-dom";
import Modal from "semantic-ui-react/dist/commonjs/modules/Modal/Modal";
import {UploadActionRequest} from "../../store/profiles/actions";

export interface IProfileUploadModalProps extends RouteComponentProps<any> {
    upload: UploadActionRequest;
}

export const ProfileUploadModal: React.FunctionComponent<IProfileUploadModalProps> = ({ history, upload }: IProfileUploadModalProps) => (
    <Modal defaultOpen onClose={() => {
        history.goBack();
    }}>
        <Modal.Header>Upload a Profile</Modal.Header>
        <Modal.Content>
            <Modal.Description>
                <Dropzone onDrop={(accepted: File[], rejected: File[]) => {
                    if (accepted.length === 0) { return; }
                    const toUpload = accepted[0];
                    upload(toUpload);
                }}>
                    {({getRootProps, getInputProps, isDragActive}) => {
                        return (
                            <div
                                {...getRootProps()}
                                >
                              <input {...getInputProps()} />
                                {
                                    isDragActive ?
                                        <p>Drop files here...</p> :
                                        <p>Try dropping some files here, or click to select files to upload.</p>
                                }
                            </div>
                        )
                    }}
                </Dropzone>
            </Modal.Description>
        </Modal.Content>
    </Modal>
);
