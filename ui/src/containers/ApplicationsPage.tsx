import * as React from "react";
import {Link, Route} from "react-router-dom";
import {connect} from "react-redux";
import {RouteComponentProps} from "react-router";
import {bindActionCreators, Dispatch} from "redux";
import {
    Container,
    Header,
    Dropdown,
    Divider,
    Breadcrumb,
} from "semantic-ui-react";

import {RootState} from "../reducers";
import {ApplicationsTable} from "../components/react-tables/ApplicationsTable";
import {IApplicationsState} from "../store/applications/list_reducer";
import {IReactTableState} from "../store/table/types";
import {FlaskFilterOperation} from "../flask-rest-jsonapi";
import {index, IndexActionRequest} from "../store/applications/actions";
import {FlaskFilter} from "../flask-rest-jsonapi";

export interface IDispatchProps {
    index: IndexActionRequest;
}

export interface IStateProps {
    applications: IApplicationsState;
}

type ApplicationsPageProps = IDispatchProps & IStateProps & RouteComponentProps<any>;

class UnconnectedApplicationsPage extends React.Component<ApplicationsPageProps, any> {
    public render() {
        const {
            applications,
        } = this.props;

        return (
            <Container className="ApplicationsPage">
                <Divider hidden/>
                <Breadcrumb>
                    <Breadcrumb.Section><Link to={`/`}>Home</Link></Breadcrumb.Section>
                    <Breadcrumb.Divider />
                    <Breadcrumb.Section>Applications</Breadcrumb.Section>
                </Breadcrumb>
                <Divider hidden/>

                <Header as="h1">Applications</Header>
                <Dropdown text="Add" icon="plus" labeled button className="icon">
                    <Dropdown.Menu>
                        <Dropdown.Item as={Link} to="/applications/add/macos">macOS Enterprise Package
                            (.pkg)</Dropdown.Item>
                        <Dropdown.Item as={Link} to="/applications/add/macSoftware">macOS App Store
                            Application</Dropdown.Item>
                        <Dropdown.Item as={Link} to="/applications/add/software">iOS App Store
                            Application</Dropdown.Item>
                        <Dropdown.Item as={Link} to="/applications/add/ios" disabled>iOS Enterprise Application
                            (.ipa)</Dropdown.Item>
                    </Dropdown.Menu>
                </Dropdown>

                <ApplicationsTable data={applications.items}
                                   loading={applications.loading}
                                   onFetchData={this.fetchData}
                />
            </Container>
        );
    }

    private fetchData = (state: IReactTableState) => {
        const sorting = state.sorted.map((value) => (value.desc ? value.id : "-" + value.id));
        const filtering: FlaskFilter[] = state.filtered.map((value) => {
            return {
                name: value.id,
                op: "ilike" as FlaskFilterOperation,
                val: `%25${value.value}%25`,
            };
        });

        this.props.index(state.pageSize, state.page, sorting, filtering);
    }
}

export const ApplicationsPage = connect(
    (state: RootState, ownProps?: any) => ({
        applications: state.applications,
    }),
    (dispatch: Dispatch, ownProps?: any) => bindActionCreators({
        index,
    }, dispatch),
)(UnconnectedApplicationsPage);
