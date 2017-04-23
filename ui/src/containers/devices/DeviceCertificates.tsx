import * as React from 'react';
import {connect, Dispatch} from 'react-redux';
import {RouteComponentProps} from 'react-router';
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

interface RouterProps {
    id: string; // device id
}

interface DeviceCertificatesProps extends ReduxStateProps, ReduxDispatchProps, RouteComponentProps<RouterProps> {

}

@connect<ReduxStateProps, ReduxDispatchProps, DeviceCertificatesProps>(
    mapStateToProps,
    mapDispatchToProps
)
export class DeviceCertificates extends React.Component<DeviceCertificatesProps, any> {

  render (): JSX.Element {
      return (
          <div>Certs</div>
      )
  }
}