import * as React from 'react';
import {connect, Dispatch} from 'react-redux';
import {RootState} from "../src/reducers/index";
import {bindActionCreators} from "redux";
import Container from "semantic-ui-react/src/elements/Container";
import Header from "semantic-ui-react/src/elements/Header";
import {DeviceGroupForm, FormData as DeviceGroupFormData} from "../src/forms/DeviceGroupForm";
import {
    post, PostActionRequest,
    read, ReadActionRequest
} from "../src/actions/device_groups";
import {RouteComponentProps} from "react-router";
import Griddle, {RowDefinition, ColumnDefinition} from 'griddle-react';
import {DeviceGroup} from "../src/models";
import {JSONAPIDetailResponse} from "../src/json-api";
import {SemanticUIPlugin} from "../src/griddle-plugins/semantic-ui/index";
import {SimpleLayout as Layout} from "../src/components/griddle/SimpleLayout";
import {Device} from "../src/store/device/types";

interface RouteProps {
    id?: string;
}

interface OwnProps extends RouteComponentProps<RouteProps> {
    handleSubmit: (values: DeviceGroupFormData) => void;
}

interface ReduxStateProps {
    device_group: JSONAPIDetailResponse<DeviceGroup, Device>;
}

function mapStateToProps(state: RootState, ownProps?: OwnProps): ReduxStateProps {
    return {
        device_group: state.device_groups.editing
    };
}

interface ReduxDispatchProps {
    post: PostActionRequest;
    read: ReadActionRequest;
}

function mapDispatchToProps(dispatch: Dispatch<RootState>, ownProps?: OwnProps) {
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
