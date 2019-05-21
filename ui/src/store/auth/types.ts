export interface IOAuth2TokenSuccessResponse {
    access_token: string;
    expires_in: number;
    token_type: "Bearer";
}
