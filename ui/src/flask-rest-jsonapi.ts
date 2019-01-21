type WrappedChildIndexActionCreator<R> = (id: string, queryParameters: string[]) => R;
type WrappedIndexActionCreator<R> = (queryParameters: string[]) => R;

export type FlaskFilterOperation = "any" | "between" | "endswith" | "eq" | "ge" | "gt" |
    "has" | "ilike" | "in_" | "is_" | "isnot" | "like" | "le" | "lt" | "match" | "ne" | "notlike" |
    "notin_" | "notlike" | "startswith";

export interface FlaskFilter {
    name: string;
    op: FlaskFilterOperation;
    val?: string;
    field?: string;
}

export type FlaskFilters = FlaskFilter[];

/**
 * This higher order function processes the standard JSON-API index action creator and provides the already encoded
 * URL query to be appended to the JSON-API endpoint URL.
 *
 * @param wrappedActionCreator
 */
export const encodeJSONAPIIndexParameters = <R>(wrappedActionCreator: WrappedIndexActionCreator<R>) => (
    size: number = 10,
    pageNumber: number = 1,
    sort?: string[],
    filters?: FlaskFilters,
    include?: string[],
) => {
    const queryParameters = [];

    queryParameters.push(`page[size]=${size}`);
    queryParameters.push(`page[number]=${pageNumber}`);

    if (sort && sort.length > 0) {
        queryParameters.push("sort=" + sort.join(","));
    }

    if (filters && filters.length > 0) {
        queryParameters.push("filter=" + JSON.stringify(filters));
    }

    if (include && include.length > 0) {
        queryParameters.push("include=" + include.join(","));
    }

    return wrappedActionCreator(queryParameters);
};
/**
 * This higher order function processes the standard JSON-API index action creator and provides the already encoded
 * URL query to be appended to the JSON-API endpoint URL.
 *
 * @param wrappedActionCreator
 */
export const encodeJSONAPIChildIndexParameters = <R>(wrappedActionCreator: WrappedChildIndexActionCreator<R>) => (
    id: string,
    size: number = 10,
    pageNumber: number = 1,
    sort?: string[],
    filters?: FlaskFilters,
) => {
    const queryParameters = [];

    queryParameters.push(`page[size]=${size}`);
    queryParameters.push(`page[number]=${pageNumber}`);

    if (sort && sort.length > 0) {
        queryParameters.push("sort=" + sort.join(","));
    }

    if (filters && filters.length > 0) {
        queryParameters.push("filter=" + JSON.stringify(filters));
    }

    return wrappedActionCreator(id, queryParameters);
};
