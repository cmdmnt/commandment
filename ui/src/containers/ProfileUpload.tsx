import * as React from "react";
import {connect} from "react-redux";
import {bindActionCreators, Dispatch} from "redux";
import {ProfileUploadModal} from "../components/modals/ProfileUploadModal";
import {RootState} from "../reducers";
import {upload, UploadActionRequest} from "../store/profiles/actions";

export interface IReduxDispatchProps {
    upload: UploadActionRequest;
}

export const ProfileUpload = connect<any, IReduxDispatchProps>(
    (state: RootState) => {
        return state.profiles;
    },
    (dispatch: Dispatch, ownProps: any) => bindActionCreators({
        upload,
    }, dispatch),
)(ProfileUploadModal);
