import * as React from "react";
import { Image, List, Grid } from "semantic-ui-react";
import {ArtworkIconSize, IiTunesSoftwareSearchResult} from "../../store/applications/itunes";
import Button from "semantic-ui-react/dist/commonjs/elements/Button";

export interface IMASResultProps {
    icon?: ArtworkIconSize;
    data: IiTunesSoftwareSearchResult;
    onClickAdd: (result: IiTunesSoftwareSearchResult) => void;
}

export const MASResult: React.FunctionComponent = ({ data, onClickAdd, icon }: IMASResultProps) => (
    <List.Item>
        <Image src={icon ? data[icon] : data.artworkUrl100} rounded />
        <List.Content>
            <List.Header>{data.trackName}</List.Header>
            <List.Description>
                <List.List>
                    <List.Item>{data.artistName}</List.Item>
                    <List.Item>Version {data.version}</List.Item>
                    <List.Item><Button size={"tiny"} onClick={() => (onClickAdd(data))}>Add</Button></List.Item>
                </List.List>
            </List.Description>
        </List.Content>
    </List.Item>
);
