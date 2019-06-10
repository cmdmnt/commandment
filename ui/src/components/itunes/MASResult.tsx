import * as React from "react";
import { Image, List, Grid, Button } from "semantic-ui-react";
import {ArtworkIconSize, IiTunesSoftwareSearchResult} from "../../store/applications/itunes";


export interface IMASResultProps {
    icon?: ArtworkIconSize;
    data: IiTunesSoftwareSearchResult;
    isAdded: boolean;
    onClickAdd: (result: IiTunesSoftwareSearchResult) => void;
}

export const MASResult: React.FunctionComponent = ({ data, onClickAdd, isAdded = false, icon }: IMASResultProps) => (
    <List.Item>
        <Image src={icon ? data[icon] : data.artworkUrl100} rounded />
        <List.Content>
            <List.Header>{data.trackName}</List.Header>
            <List.Description>
                <List.List>
                    <List.Item>{data.artistName}</List.Item>
                    <List.Item>Version {data.version}</List.Item>
                </List.List>
            </List.Description>
        </List.Content>
        <List.Content>
            <List.Description>
                <Button size={"tiny"} disabled={isAdded} onClick={() => (onClickAdd(data))}>{isAdded ? "Added" : "Add"}</Button>
            </List.Description>
        </List.Content>
    </List.Item>
);
