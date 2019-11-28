# FAQ

I'm getting "gcasc.ClientInitializationError: GitLab token was not provided. It must be defined in 
`GITLAB_CLIENT_TOKEN` environment variable"

   >It is likely that you provided invalid GitLab client configuration. If you use configuration file, verify
    if it has all required configuration parameters and that ``GITLAB_CLIENT_CONFIG_FILE`` environment variable
    is set to a path where your config file is. If you use environment variables, verify that you provided
    all necessary variables.
    See the :ref:`client configuration <client_configuration>` for details.