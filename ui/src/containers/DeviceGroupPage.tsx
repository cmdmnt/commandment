import * as React from 'react';
import {connect, Dispatch} from 'react-redux';
import {IRootState} from "../reducers/index";
import {bindActionCreators} from "redux";
import {Container, Segment, Header} from 'semantic-ui-react';
import {DeviceGroupForm, FormData as DeviceGroupFormData} from "../forms/DeviceGroupForm";
import {
    post, PostActionRequest,
    read, ReadActionRequest
} from "../actions/device_groups";
import {RouteComponentProps} from "react-router";
import Griddle, {RowDefinition, ColumnDefinition} from 'griddle-react';
import {Device, DeviceGroup} from "../models";
import {JSONAPIDetailResponse} from "../json-api";
import {SemanticUIPlugin} from "../griddle-plugins/semantic-ui/index";
import {SimpleLayout as Layout} from "../components/griddle/SimpleLayout";

interface RouteProps {
    id?: string;
}

interface OwnProps extends RouteComponentProps<RouteProps> {
    handleSubmit: (values: DeviceGroupFormData) => void;
}

interface ReduxStateProps {
    device_group: JSONAPIDetailResponse<DeviceGroup, Device>;
}

function mapStateToProps(state: IRootState, ownProps?: OwnProps): ReduxStateProps {
    return {
        device_group: state.device_groups.editing
    };
}

interface ReduxDispatchProps {
    post: PostActionRequest;
    read: ReadActionRequest;
}

function mapDispatchToProps(dispatch: Dispatch<IRootState>, ownProps?: OwnProps) {
    return bindActionCreators({
        post,
        read
    }, dispatch);
}


class BaseDeviceGroupPage extends React.Component<ReduxStateProps & ReduxDispatchProps & OwnProps, void> {

    componentWillMount?() {
        if (this.props.match.params.id) {
            this.props.read(this.props.match.params.id, ['devices']);
        }
    }

    handleSubmit = (values: DeviceGroupFormData) => {
        if (this.props.match.params.id) {
            // this.props.patch()
        } else {
            this.props.post(values);
        }
    };

    render() {
        const {
            device_group
        } = this.props;

        let initialValues: any;
        if (device_group) {
            initialValues = device_group.data.attributes;
        }

        return (
            <Container>
                <Header as='h1'>Device Group</Header>
                <DeviceGroupForm onSubmit={this.handleSubmit} initialValues={initialValues}/>
                <Header as='h2'>Members</Header>
                <Griddle
                    plugins={[SemanticUIPlugin()]}
                    styleConfig={{
                        classNames: {
                            Table: 'ui celled table',
                            NoResults: 'ui message'
                        }
                    }}
                    components={{Layout}}
                >

                </Griddle>
            </Container>
        )
    }
}

export const DeviceGroupPage = connect<ReduxStateProps, ReduxDispatchProps, OwnProps>(
    mapStateToProps, mapDispatchToProps)(BaseDeviceGroupPage);
