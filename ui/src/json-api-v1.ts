
export const ContentType = "application/vnd.api+json";

export type Link = string | { href?: string, meta?: { [index: string]: any }};

export interface Links {
    self?: Link;
    related?: Link;

    // Pagination
    first?: Link;
    last?: Link;
    prev?: Link;
    next?: Link;
}

// http://jsonapi.org/format/#errors
export interface ErrorObject {
    id?: any;
    links?: {
        about?: string;
    };
    status?: string;
    code?: string;
    title?: string;
    detail?: string;
    source?: {
        pointer?: string;
        parameter?: string;
    };
    meta?: any;
}

export interface ErrorResponse {
    errors: ErrorObject[];
    jsonapi: {
        version: string;
    };
}

export interface ResourceIdentifier {
    type: string;
    id: string;
    meta?: any;
}

export type RelationshipData = ResourceIdentifier[] | ResourceIdentifier | null;

export interface Relationship {
    data: RelationshipData,
    links: Links;
    meta?: any;
}

export interface Relationships {
    [relationshipName: string]: Relationship;
}

export type PrimaryData = ResourceObject<any> | Array<ResourceObject<any>> | null | any[] |
    ResourceIdentifier | ResourceIdentifier[];

export interface DataResponse<TData, TIncluded> {
    data?: TData;
    included?: TIncluded;
    links?: Links;
    meta?: {
        count?: number;
    };
    jsonapi?: {
        version: string;
    };
}

export interface ResourceObject<TAttributes> {
    id: string|number;
    type: string;
    attributes?: TAttributes;
    relationships?: Relationships;
    links?: Links;
    meta?: any;
}

export interface CreateResourceObject<TAttributes> {
    type: string;
    attributes?: TAttributes;
    relationships?: Relationships;
    links?: Links;
    meta?: any;
}

export type JSONAPIDocument<TData = any, TIncluded = any> = DataResponse<TData, TIncluded> | ErrorResponse;

export function isErrorResponse(value: JSONAPIDocument): value is ErrorResponse {
    return value.hasOwnProperty("errors");
}
