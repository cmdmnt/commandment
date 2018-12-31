import * as React from "react";
import {connect} from "react-redux";
import {ProfileUploadModal} from "../components/modals/ProfileUploadModal";
import {RootState} from "../reducers";
import {bindActionCreators, Dispatch} from "redux";
import {upload, UploadActionRequest} from "../store/profiles/actions";

export interface IReduxStateProps {

}

export interface IReduxDispatchProps {
    upload: UploadActionRequest;
}

export const ProfileUpload = connect<IReduxStateProps, IReduxDispatchProps>(
    (state: RootState) => {
        return state.profiles;
    },
    (dispatch: Dispatch, ownProps: any) => bindActionCreators({
        upload,
    }, dispatch),
)(ProfileUploadModal);
