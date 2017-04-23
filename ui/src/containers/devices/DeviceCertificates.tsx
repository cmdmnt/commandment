import * as React from 'react';
import {connect, Dispatch} from 'react-redux';
import {RootState} from "../../reducers/index";

interface ReduxStateProps {
    items: Array<JSONAPIObject<InstalledCertificate>>;
}

function mapStateToProps(state: RootState, ownProps?: any): ReduxStateProps {
    return {
        items: state.device.certificates.items
    }
}

interface ReduxDispatchProps {

}

function mapDispatchToProps(dispatch: Dispatch<any>): ReduxDispatchProps {
    return {};
}

interface DeviceCertificatesProps extends ReduxStateProps, ReduxDispatchProps {

}

@connect<ReduxStateProps, ReduxDispatchProps, DeviceCertificatesProps>(
    mapStateToProps,
    mapDispatchToProps
)
export class DeviceCertificates extends React.Component<DeviceCertificatesProps, undefined> {

  render (): JSX.Element {
      return (
          <div>Certs</div>
      )
  }
}