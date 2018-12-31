
export interface IReactTableState {
    page: number;
    pageSize: number;
    filtered: Array<{ id: string; value: any; }>;
    sorted: Array<{ id: string; desc: boolean; }>;
}
