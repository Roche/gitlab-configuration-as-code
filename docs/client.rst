.. _client_configuration:

###########################
Client Configuration
###########################

| **Environment variable**    | **Description**                                                                                                                  | **Default value**                | **Example**                     |
|-----------------------------|----------------------------------------------------------------------------------------------------------------------------------|----------------------------------|---------------------------------|
| `GITLAB_CLIENT_API_VERSION` | Version of GitLab API. Current latest: `4`                                                                                       | `4`                              | `4`                             |
| `GITLAB_CLIENT_CONFIG_FILE` | Path to GitLab client configuration                                                                                              | `/etc/gitlab.cfg, ~/.gitlab.cfg` | `/home/myuser/gitlabclient.cfg` |
| `GITLAB_CLIENT_URL`         | URL to GitLab instance. Used only if `GITLAB_CLIENT_CONFIG_FILE` not provided or invalid.                                        | `https://gitlab.com`             | `https://mygitlab.mydomain.com` |
| `GITLAB_CLIENT_SSL_VERIFY`  | Flag if SSL certificate of GitLab instance should be verified. Used only if `GITLAB_CLIENT_CONFIG_FILE` not provided or invalid. | `true`                           | `false`                         |
| `GITLAB_CLIENT_TOKEN`       | **Required**. Private token used to access GitLab API. Used only if `GITLAB_CLIENT_CONFIG_FILE` not provided or invalid.         |                                  | `-uub91Jax13P1iaLkC3za0`        |
| `GITLAB_CLIENT_CERT`        | Path to client certificate used for mutual TLS authentication to access GitLab API.                                              |                                  | `/home/myuser/client.crt`       |
| `GITLAB_CLIENT_KEY`         | Path to client key used for mutual TLS authentication to access GitLab API.                                                      |                                  | `/home/myuser/key.pem`          |
