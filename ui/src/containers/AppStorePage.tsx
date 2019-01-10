import * as React from "react";
import Container from "semantic-ui-react/dist/commonjs/elements/Container/Container";
import Divider from "semantic-ui-react/dist/commonjs/elements/Divider/Divider";
import Header from "semantic-ui-react/dist/commonjs/elements/Header/Header";
import {List} from "semantic-ui-react";

import {connect} from "react-redux";
import {RouteComponentProps} from "react-router";
import {bindActionCreators, Dispatch} from "redux";
import {MASResult} from "../components/itunes/MASResult";
import {SearchInput} from "../components/SearchInput";
import {RootState} from "../reducers";
import {
    itunesSearch, ItunesSearchAction,
    post, PostActionRequest,
} from "../store/applications/actions";
import {
    ArtworkIconSize,
    EntityType,
    IiTunesSearchResult,
    IiTunesSoftwareSearchResult,
    MediaType,
} from "../store/applications/itunes";

interface IRouteProps {
    entity: EntityType;
}

export interface IDispatchProps {
    itunesSearch: ItunesSearchAction;
    post: PostActionRequest;
}

export interface IStateProps {
    storeCountry: string;
    loading: boolean;
    itunesSearchResult: IiTunesSearchResult;
}

export type AppStorePageProps = IDispatchProps & IStateProps & RouteComponentProps<IRouteProps>;

export class UnconnectedAppStorePage extends React.Component<AppStorePageProps, any> {

    // public static initialState: IAppStorePageState = {
    //     term: "",
    // };

    public render() {
        const { itunesSearchResult, loading } = this.props;

        return (
            <Container>
                <Divider hidden/>
                <Header as="h1">App Store</Header>

                <SearchInput duration={400} loading={loading} onSearch={this.handleSearch}/>

                {itunesSearchResult &&
                    <List relaxed="very">
                        {itunesSearchResult.results.map((result: IiTunesSoftwareSearchResult) => (
                            <MASResult key={result.trackId}
                                       data={result}
                                       icon={ArtworkIconSize.Sixty}
                                       onClickAdd={this.handleClickAdd} />
                        ))}
                    </List>
                }
            </Container>
        );
    }

    private handleClickAdd = (result: IiTunesSoftwareSearchResult) => {
        this.props.post({
            bundle_id: result.bundleId,
            description: result.description,
            display_name: result.trackName,
            itunes_store_id: result.trackId,
            version: result.version,

            country: this.props.storeCountry,

            artist_id: result.artistId,
            artist_name: result.artistName,
            artist_view_url: result.artistViewUrl,
            artwork_url60: result.artworkUrl60,
            artwork_url100: result.artworkUrl100,
            artwork_url512: result.artworkUrl512,
            release_notes: result.releaseNotes,
            release_date: result.releaseDate,
            minimum_os_version: result.minimumOsVersion,
            file_size_bytes: result.fileSizeBytes,
        });
    };

    private handleSearch = (value: string) => {
        const { match: { params: { entity }}, storeCountry} = this.props;
        this.props.itunesSearch(value, storeCountry, MediaType.software, entity);
    };
}

export const AppStorePage = connect(
    (state: RootState, ownProps?: any) => ({
        itunesSearchResult: state.applications.itunesSearchResult,
        loading: state.applications.itunesSearchResultLoading,
        storeCountry: state.applications.storeCountry,
    }),
    (dispatch: Dispatch, ownProps?: any) => bindActionCreators({
        itunesSearch,
        post,
    }, dispatch),
)(UnconnectedAppStorePage);
