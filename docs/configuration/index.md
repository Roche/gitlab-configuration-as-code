# Configuration

* [Appearance](../appearance.md)
* [Application Settings](../application_settings.md)
* [License](../license.md)

GitLab configuration is defined in a [YAML](https://docs.ansible.com/ansible/latest/reference_appendices/YAMLSyntax.html).
Providing configuraton for your GitLab instance is as simple as this:
```yaml
appearance:
  title: "Your GitLab instance title"
  logo: "http://path-to-your-logo/logo.png"

settings:
  elasticsearch:
    url: http://elasticsearch.mygitlab.com
    username: !env ELASTICSEARCH_USERNAME
    password: !env ELASTICSEARCH_PASSWORD
  recaptcha_enabled: yes
  terms: !include toc.md
  plantuml:
    enabled: true
    url: 'http://plantuml.url'

license:
  starts_at: 2019-11-17
  expires_at: 2019-12-17
  plan: premium
  user_limit: 30
  data: !include gitlab.lic
```

You can customize where _GCasC_ searches for configuration file or if any changes should be applied on instance
using environment variables.

| **Environment variable**    | **Description**                                                                           | **Default value**                | **Example**                     |
|-----------------------------|-------------------------------------------------------------------------------------------|----------------------------------|---------------------------------|
| `GITLAB_CONFIG_FILE`        | Path to GitLab main configuration. It is<br/>our Configuration as Code entry point.           | `./gitlab.yml`                   | `/home/myuser/gitlabconf.yml`   |
| `GITLAB_MODE`               | Determine if any changes, when detected,<br/>should be applied. Valid values: `APPLY`, `TEST` | `APPLY`                          | `TEST`                          |

**Yaml directives**

Custom Yaml directives give you enhanced way of defining your GitLab configuration YAML, where you can
split your configuration into multiple Yaml files or inject environment variables.

* `!include` to provide path to another Yaml or plain text file which will be included file 
under certain key, e.g.
    ```yaml
    settings:
      terms: !include toc.md
      elasticsearch: !include config/elasticsearch.yml
    ```
  
* `!env` to inject values of environment variables under certain key, e.g.
    ```yaml
    settings:
      elasticsearch_username: !env ELASTICSEARCH_USERNAME
      elasticsearch_password: !env ELASTICSEARCH_PASSWORD
    ```
  
**Note:** Use `!env` directive to inject secrets into your Yaml. Never put secrets directly in Yaml file!