# Client Configuration

You can configure GitLab client using multiple methods and configuration settings will be searched in the following
order:

* configuration file
* environment variables

**Important!** GitLab does not allow authentication using API with username and password. The preferred approach
is to use personal access tokens. For more about it see [getting personal access token](#getting-personal-access-token).

## Configuration file

Configuration file can have any name, but must contain have following structure (do not omit `[global]` line):

 ```bash
[global]
url = https://gitlab.yourdomain.com
ssl_verify = true  # optional
timeout = 5  # optional
private_token = <personal_access_token>
api_version = 4  # optional, assumes latest
 ```

By default _GCasC_ is trying to find client configuration file in following paths:
```bash
/etc/python-gitlab.cfg
/etc/gitlab.cfg
~/.python-gitlab.cfg
~/.gitlab.cfg
```
 
You can provide another path to your configuration file in `GITLAB_CLIENT_CONFIG_FILE` environment variable.

## Environment variables

You can use set up environment variables to configure your API client:

| **Environment variable**    | **Description**                                                                                                                  | **Default value**                | **Example**                     |
|-----------------------------|----------------------------------------------------------------------------------------------------------------------------------|----------------------------------|---------------------------------|
| `GITLAB_CLIENT_API_VERSION` | Version of GitLab API. Current latest: `4`                                                                                       | `4`                              | `4`                             |
| `GITLAB_CLIENT_URL`         | URL to GitLab instance. Used only if <br/>`GITLAB_CLIENT_CONFIG_FILE` not provided or invalid.                                        | `https://gitlab.com`             | `https://mygitlab.mydomain.com` |
| `GITLAB_CLIENT_SSL_VERIFY`  | Flag if SSL certificate of GitLab instance<br/>should be verified. Used only if `GITLAB_CLIENT_CONFIG_FILE`<br/>not provided or invalid. | `true`                           | `false`                         |
| `GITLAB_CLIENT_TOKEN`       | **Required**. Private token used to access<br/>GitLab API. Used only if `GITLAB_CLIENT_CONFIG_FILE`<br/>not provided or invalid.         |                                  | `-uub91Jax13P1iaLkC3za0`        |

## Getting personal access token

You **must** have personal access token if you want to use _GCasC_. Personal access token is mandatory in any client
configuration approach. Unfortunately there is no way to configure it via API or get it automatically on instance setup.
Thus you must first have GitLab running (for fresh deploys), then go to the UI and follow
[these instructions](https://docs.gitlab.com/ee/user/profile/personal_access_tokens.html) to get personal access token.

Recommendation is to limit scopes to minimal set required by the token. Additionally limit the time how long token
is valid. It may not be the most convenient approach for CI/CD pipelines, but gives you additional significant security.

## Setting client certificate`

_GCasC_ allows setting up client certificate in case your GitLab instance requires mutual TLS authentication.
You can configure it same way when using either configuration file or environment variables for client.

Just provide both of these environment variables. If one of them is missing, error will be raised.

| **Environment variable**    | **Description**                                                                         | **Example**               |
|-----------------------------|-----------------------------------------------------------------------------------------|---------------------------|
| `GITLAB_CLIENT_CERT`        | Path to client certificate used for mutual TLS<br/>authentication to access GitLab API. | `/home/myuser/client.crt` |
| `GITLAB_CLIENT_KEY`         | Path to client key used for mutual TLS</br>authentication to access GitLab API.         | `/home/myuser/key.pem`    |
