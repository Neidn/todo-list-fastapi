async def get_current_user(
        security_scopes: SecurityScopes,
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_database_session),
) -> User:
    # Check Current User
    credentials_exception = __build_credential_exception(security_scopes.scope_str)
