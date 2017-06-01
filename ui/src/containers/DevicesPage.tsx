import * as React from 'react';
import {connect, Dispatch} from 'react-redux';
import Griddle, {RowDefinition, ColumnDefinition} from 'griddle-react';
import {Grid, Header, Container} from 'semantic-ui-react'

import {bindActionCreators, Store} from "redux";
import * as actions from '../actions/devices';
import {RootState} from "../reducers/index";
import {RouteComponentProps} from "react-router";
import {DevicesState} from "../reducers/devices";
import {IndexActionRequest} from "../actions/devices";
import {ModelIcon} from '../components/ModelIcon';
import {DeviceLink} from '../components/griddle/DeviceLink';
import {SinceNowUTC} from "../components/griddle/SinceNowUTC";
import {SimpleLayout} from '../components/griddle/SimpleLayout';
import {SelectionPlugin} from '../griddle-plugins/selection';
import {DeviceColumn} from "../components/griddle/DeviceColumn";
import {MultiAttrCellPlugin} from "../griddle-plugins/multiattr-cell/index";
import {SemanticUIPlugin} from "../griddle-plugins/semantic-ui/index";


const rowDataSelector = (state: any, { griddleKey }: { griddleKey: string }) => {
    return state
        .get('data')
        .find(rowMap => rowMap.get('griddleKey') === griddleKey)
        .toJSON();
};

const enhancedWithRowData = connect((state, props) => {
    return {
        // rowData will be available into MyCustomComponent
        rowData: rowDataSelector(state, props)
    };
});

interface ReduxStateProps {
    devices: DevicesState;
}

function mapStateToProps(state: RootState, ownProps?: any): ReduxStateProps {
    return {devices: state.devices};
}

interface ReduxDispatchProps {
    index: IndexActionRequest;
}

function mapDispatchToProps(dispatch: Dispatch<any>): ReduxDispatchProps {
    return bindActionCreators({
        index: actions.index
    }, dispatch);
}

interface DevicesPageProps extends ReduxStateProps, ReduxDispatchProps, RouteComponentProps<any> {
    componentWillMount: () => void;
}

interface DevicesPageState {
    filter: string;
}

@connect<ReduxStateProps, ReduxDispatchProps, DevicesPageProps>(
    mapStateToProps,
    mapDispatchToProps
)
export class DevicesPage extends React.Component<DevicesPageProps, DevicesPageState> {

    componentWillMount?(): void {
        this.props.index();
    }

    handleFilter = (filterText: string) => {
        // TODO: debounce filter text
    };

    handleSort = (sortProperties: { id: string; }) => {
        console.dir(sortProperties);
    };

    handleNextPage = () => {

    };

    handlePrevPage = () => {

    };

    handleGetPage = (pageNumber: number) => {
        console.log(pageNumber);
    };

    render(): JSX.Element {
        const {
            devices
        } = this.props;

        const eventHandlers = {
            onFilter: this.handleFilter,
            onSort: this.handleSort,
            onNext: this.handleNextPage,
            onPrev: this.handlePrevPage,
            onGetPage: this.handleGetPage
        };

        return (
            <Container className='DevicesPage'>
                <Grid>
                    <Grid.Column>
                        <Header as="h1">Devices</Header>

                        <Griddle
                            data={devices.items}
                            pageProperties={{
                                currentPage: devices.currentPage,
                                pageSize: devices.pageSize,
                                recordCount: devices.recordCount
                            }}
                            styleConfig={{
                                classNames: {
                                    Table: 'ui celled table'
                                }
                            }}
                            events={eventHandlers}
                            plugins={[SemanticUIPlugin(), SelectionPlugin()]}
                            components={{
                                Layout: SimpleLayout
                            }}
                        >
                            <RowDefinition onClick={() => console.log('fmeh')}>
                                <ColumnDefinition title='Device' id="id,attributes.model_name,attributes.device_name"
                                                  customComponent={enhancedWithRowData(DeviceColumn)}/>

                                <ColumnDefinition title="Last Seen" id="attributes.last_seen"
                                                  customComponent={SinceNowUTC}/>
                            </RowDefinition>
                        </Griddle>
                    </Grid.Column>
                </Grid>
            </Container>
        );
    }
}