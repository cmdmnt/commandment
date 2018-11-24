import * as React from "react";
import {Link} from "react-router-dom";
import {JSONAPIDataObject} from "../../json-api";
import {DEPProfile} from "../../store/dep/types";

interface IDEPProfileColumnProps {
    rowData: JSONAPIDataObject<DEPProfile>;
}

export class DEPProfileColumn extends React.Component<IDEPProfileColumnProps, undefined> {
    public render() {
        const {
            rowData,
        } = this.props;

        const depAccount = rowData.relationships.dep_account;

        return (
            <div>
                <Link to={`/dep/accounts/${depAccount.data.id}/profiles/${rowData.id}`}>
                    <span>{ rowData.attributes.profile_name }</span>
                </Link>
            </div>
        )
    }
}
