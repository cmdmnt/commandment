import * as React from "react";
import {Input, InputOnChangeData, InputProps} from "semantic-ui-react";
import Timeout = NodeJS.Timeout;

export interface ISearchInputProps {
    duration: number;
    loading: boolean;
    onSearch: (value: string) => void;
}

export interface ISearchInputState {
    value: string;
    timeout: Timeout;
}

export class SearchInput extends React.Component<ISearchInputProps, ISearchInputState> {

    // public static initialState: ISearchInputState = {
    //     timeout: null,
    //     value: "",
    // };
    constructor(props: ISearchInputProps) {
        super(props);
        this.state = { timeout: null, value: "" };
    }

    public render() {
        const { loading } = this.props;

        return (
            <Input loading={loading ? true : undefined}
                   icon="search"
                   placeholder="App Name..."
                   onChange={this.handleChange}
                   value={this.state.value}
            />
        )
    }

    private handleTimeout = (e: any) => {
        this.props.onSearch(this.state.value);
        this.setState({ timeout: null });
    };

    private handleChange = (event: any, data: InputOnChangeData) => {
        if (this.state.timeout) {
            clearTimeout(this.state.timeout);
        }

        const timeout = setTimeout(this.handleTimeout, this.props.duration | 400);
        this.setState({ timeout, value: data.value });
    };
}
