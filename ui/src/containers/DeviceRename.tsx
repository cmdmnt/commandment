import * as React from "react";
import {connect} from "react-redux";
import {bindActionCreators, Dispatch} from "redux";
import {DeviceRenameModal} from "../components/modals/DeviceRenameModal";
import {RootState} from "../reducers";
import {upload, UploadActionRequest} from "../store/profiles/actions";

export interface IReduxStateProps {

}

export interface IReduxDispatchProps {

}

export const DeviceRename = connect<IReduxStateProps, IReduxDispatchProps>(
    (state: RootState) => {
        return state.device;
    },
    (dispatch: Dispatch, ownProps: any) => bindActionCreators({
        upload,
    }, dispatch),
)(DeviceRenameModal);
