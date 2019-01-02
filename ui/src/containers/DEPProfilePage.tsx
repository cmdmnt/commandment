import * as React from "react";

import {connect, Dispatch} from "react-redux";
import {RouteComponentProps} from "react-router";
import {Link} from "react-router-dom";
import {bindActionCreators} from "redux";
import {AccordionTitleProps} from "semantic-ui-react";
import Breadcrumb from "semantic-ui-react/dist/commonjs/collections/Breadcrumb/Breadcrumb";
import Container from "semantic-ui-react/dist/commonjs/elements/Container/Container";
import Header from "semantic-ui-react/dist/commonjs/elements/Header/Header";
import {DEPProfileForm, IDEPProfileFormValues} from "../components/forms/DEPProfileForm";
import {RSAAApiErrorMessage} from "../components/RSAAApiErrorMessage";
import {RootState} from "../reducers";
import {
    patchProfile,
    postProfile,
    profile, ProfilePatchActionRequest,
    ProfilePostActionRequest,
    ProfileReadActionRequest,
} from "../store/dep/actions";
import {IDEPProfileState} from "../store/dep/profile_reducer";
import {DEPProfile, SkipSetupSteps} from "../store/dep/types";
import Divider from "semantic-ui-react/dist/commonjs/elements/Divider";

interface IReduxStateProps {
    dep_profile?: IDEPProfileState;
}

interface IReduxDispatchProps {
    getDEPProfile: ProfileReadActionRequest;
    postDEPProfile: ProfilePostActionRequest;
    patchDEPProfile: ProfilePatchActionRequest;
}

interface IRouteParameters {
    account_id: string;
    id?: string;
}

interface IDEPProfilePageProps extends IReduxStateProps, IReduxDispatchProps, RouteComponentProps<IRouteParameters> {

}

interface IDEPProfilePageState {
    activeIndex: string | number;
}

class UnconnectedDEPProfilePage extends React.Component<IDEPProfilePageProps, IDEPProfilePageState> {

    constructor(props: IDEPProfilePageProps) {
        super(props);
        this.state = {
            activeIndex: 0,
        };
    }

    public componentWillMount() {
        const {
            match: {
                params: {
                    id,
                },
            },
        } = this.props;

        if (id) {
            this.props.getDEPProfile(this.props.match.params.id);
        }
    }

    public render() {
        const {
            dep_profile,
            match: {
                params: {
                    id,
                    account_id,
                },
            },
        } = this.props;

        let title = "loading";
        let breadcrumbTitle = "DEP Profile";

        if (id) {
            title = `Edit ${this.props.dep_profile.dep_profile ?
                this.props.dep_profile.dep_profile.attributes.profile_name : "Loading..."}`;

            if (dep_profile.dep_profile) {
                dep_profile.dep_profile.attributes.show = {};
                breadcrumbTitle = dep_profile.dep_profile.attributes.profile_name;
                for (const kskip in SkipSetupSteps) {
                    if (dep_profile.dep_profile.attributes.skip_setup_items.indexOf(kskip) !== -1) {
                        dep_profile.dep_profile.attributes.show[kskip] = false;
                    } else {
                        dep_profile.dep_profile.attributes.show[kskip] = true;
                    }
                }
            }
        } else {
            title = "Create a new DEP Profile";
        }

        return (
            <Container className="DEPProfilePage">
                <Divider hidden />
                <Breadcrumb>
                    <Breadcrumb.Section><Link to={`/`}>Home</Link></Breadcrumb.Section>
                    <Breadcrumb.Divider />
                    <Breadcrumb.Section><Link to={`/dep/accounts/${account_id}`}>DEP Account</Link></Breadcrumb.Section>
                    <Breadcrumb.Divider />
                    <Breadcrumb.Section active>{ breadcrumbTitle }</Breadcrumb.Section>
                </Breadcrumb>

                <Header as="h1">{title}</Header>
                {dep_profile.error && <RSAAApiErrorMessage error={dep_profile.errorDetail} />}
                <DEPProfileForm onSubmit={this.handleSubmit}
                                loading={dep_profile.loading}
                                isSubmitting={dep_profile.loading}
                                data={dep_profile.dep_profile && dep_profile.dep_profile.attributes}
                                id={dep_profile.dep_profile && dep_profile.dep_profile.id}
                                activeIndex={this.state.activeIndex}
                                onClickAccordionTitle={this.handleAccordionClick}
                />
            </Container>
        );
    }

    private handleSubmit = (values: IDEPProfileFormValues) => {
        const { show, ...profile } = values;
        profile.skip_setup_items = [];

        if (show) {
            for (const kskip in SkipSetupSteps) {
                if (!show[kskip]) {
                    profile.skip_setup_items.unshift(kskip as SkipSetupSteps);
                }
            }
        }

        if (this.props.match.params.id) {
            this.props.patchDEPProfile(this.props.match.params.id, profile);
        } else {
            this.props.postDEPProfile(profile, {
                dep_account: {type: "dep_accounts", id: this.props.match.params.account_id},
            });
        }
    };

    private handleAccordionClick = (event: React.MouseEvent<any>, data: AccordionTitleProps) => {
        this.setState({ activeIndex: data.index });
    };
}

export const DEPProfilePage = connect(
    (state: RootState, ownProps: any): IReduxStateProps => {
        return {dep_profile: state.dep.profile};
    },
    (dispatch: Dispatch<RootState>, ownProps?: any): IReduxDispatchProps => bindActionCreators({
        getDEPProfile: profile,
        patchDEPProfile: patchProfile,
        postDEPProfile: postProfile,
    }, dispatch),
)(UnconnectedDEPProfilePage);
