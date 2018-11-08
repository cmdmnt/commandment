import * as React from 'react';
import {Link} from 'react-router-dom';
import {DEPAccount} from "../../models";
import {JSONAPIDataObject} from "../../json-api";


interface DEPAccountColumnProps {
    rowData: JSONAPIDataObject<DEPAccount>;
}

export class DEPAccountColumn extends React.Component<DEPAccountColumnProps, undefined> {
    render () {
        const {
            rowData
        } = this.props;

        return (
            <div>
                <Link to={`/dep/accounts/${rowData.id}`}>
                    <span>{ rowData.attributes.server_name }</span>
                </Link>
            </div>
        )
    }
}
