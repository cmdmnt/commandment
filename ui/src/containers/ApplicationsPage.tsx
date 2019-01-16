import * as React from "react";
import {Link, Route} from "react-router-dom";
import {connect} from "react-redux";
import {RouteComponentProps} from "react-router";
import {bindActionCreators, Dispatch} from "redux";
import Container from "semantic-ui-react/dist/commonjs/elements/Container/Container";
import {RootState} from "../reducers";
import Grid from "semantic-ui-react/dist/commonjs/collections/Grid/Grid";
import Header from "semantic-ui-react/dist/commonjs/elements/Header/Header";
import {ButtonLink} from "../components/semantic-ui/ButtonLink";
import Dropdown from "semantic-ui-react/dist/commonjs/modules/Dropdown/Dropdown";
import Divider from "semantic-ui-react/dist/commonjs/elements/Divider/Divider";
import {ApplicationsTable} from "../components/react-tables/ApplicationsTable";
import {IApplicationsState} from "../store/applications/reducer";
import {IReactTableState} from "../store/table/types";
import {FlaskFilter, FlaskFilterOperation} from "../store/constants";
import {index, IndexActionRequest} from "../store/applications/actions";
import {Breadcrumb} from "semantic-ui-react";

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
