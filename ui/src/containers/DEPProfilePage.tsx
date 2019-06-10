import * as React from "react";

import {connect} from "react-redux";
import {RouteComponentProps} from "react-router";
import {Link} from "react-router-dom";
import {bindActionCreators, Dispatch} from "redux";
import {
    AccordionTitleProps,
    Breadcrumb,
    Container,
    Header,
    Divider,
} from "semantic-ui-react";

import {DEPProfileForm, IDEPProfileFormValues} from "../components/forms/DEPProfileForm";
import {RSAAApiErrorMessage} from "../components/RSAAApiErrorMessage";
import {RootState} from "../reducers";
import {
    patchProfile,
    postProfile,
    profile, ProfilePatchActionRequest,
    ProfilePostActionCreator,
    ProfileReadActionCreator,
} from "../store/dep/actions";
import {IDEPProfileState} from "../store/dep/profile_reducer";
import {DEPProfile, SkipSetupSteps} from "../store/dep/types";
import {JSONAPIDataObject} from "../store/json-api";

interface IReduxStateProps {
    dep_profile?: IDEPProfileState;
}

interface IReduxDispatchProps {
    getDEPProfile: ProfileReadActionCreator;
    postDEPProfile: ProfilePostActionCreator;
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
        let formValues: IDEPProfileFormValues = {};

        if (id) {
            title = `Edit ${this.props.dep_profile.dep_profile ?
                this.props.dep_profile.dep_profile.attributes.profile_name : "Loading..."}`;

            if (dep_profile.dep_profile) {
                breadcrumbTitle = dep_profile.dep_profile.attributes.profile_name;
                formValues = this.profileToForm(dep_profile.dep_profile);
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
                                data={formValues}
                                id={dep_profile.dep_profile && dep_profile.dep_profile.id}
                                activeIndex={this.state.activeIndex}
                                onClickAccordionTitle={this.handleAccordionClick}
                />
            </Container>
        );
    }

    private handleSubmit = (values: IDEPProfileFormValues) => {
        const profile = this.formToProfile(values);

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

    private formToProfile = (formValues: IDEPProfileFormValues): DEPProfile => {
        const skipSetupSteps: SkipSetupSteps[] = [];
        const { show, ...attrs } = formValues;

        for (const kskip in SkipSetupSteps) {
            if (SkipSetupSteps.hasOwnProperty(kskip)) {
                if (!show[kskip]) {
                    skipSetupSteps.unshift(kskip as SkipSetupSteps);
                }
            }
        }

        return {
            ...attrs,
            skip_setup_items: skipSetupSteps,
        };
    };

    private profileToForm = (profile: JSONAPIDataObject<DEPProfile>): IDEPProfileFormValues => {
        const show: { [propName: string]: boolean } = {};
        const { skip_setup_items, ...attrs } = profile.attributes;

        for (const kskip in SkipSetupSteps) {
            if (SkipSetupSteps.hasOwnProperty(kskip)) {
                show[kskip] = skip_setup_items.indexOf(kskip as SkipSetupSteps) === -1;
            }
        }
        return {
            ...attrs,
            show,
        };
    }

}

export const DEPProfilePage = connect(
    (state: RootState, ownProps: any): IReduxStateProps => {
        return {dep_profile: state.dep.profile};
    },
    (dispatch: Dispatch, ownProps?: any): IReduxDispatchProps => bindActionCreators({
        getDEPProfile: profile,
        patchDEPProfile: patchProfile,
        postDEPProfile: postProfile,
    }, dispatch),
)(UnconnectedDEPProfilePage);
