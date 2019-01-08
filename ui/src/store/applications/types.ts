// valid relationship types
export type ApplicationRelationship = "tags";

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

    country: string;
    artist_id: number;
    artist_name: string;
    artist_view_url: string;
    artwork_url60: string;
    artwork_url100: string;
    artwork_url512: string;
    release_notes: string;
    release_date: string;
    minimum_os_version: string;
    file_size_bytes: number;
}
