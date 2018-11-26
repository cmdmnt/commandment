export interface Application {
    id?: string;
    itunes_store_id?: number;
    bundle_id?: string;
    purchase_method?: number;
    manifest_url: string;
    management_flags: number;
    change_management_state: "Managed" | null;
    display_name: string;
    description: string;
    version: string;
}
