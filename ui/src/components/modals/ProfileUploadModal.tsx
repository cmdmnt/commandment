import * as React from "react";
import Dropzone, {DropFilesEventHandler} from "react-dropzone";
import Modal from "semantic-ui-react/dist/commonjs/modules/Modal/Modal";
import {RouteComponentProps} from "react-router-dom";

export interface IProfileUploadModal extends RouteComponentProps {

}

export const ProfileUploadModal: React.StatelessComponent = ({ onDrop, history, upload }: IProfileUploadModal) => (
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
