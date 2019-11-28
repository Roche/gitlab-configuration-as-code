# Application Settings

_GCasC_ allows configuring Application Settings. It consists of plenty of configuration options, that can be set only
through UI or API. They are key to make your GitLab instance work as you intend to.

**Reference:** https://docs.gitlab.com/12.4/ee/api/settings.html

Settings the structure is flexible. It starts with a root key `settings`. Then you provide
configuration options as defined in [these docs](https://docs.gitlab.com/12.4/ee/api/settings.html). For example

```yaml
settings:
  elasticsearch:
    url: http://elasticsearch.mygitlab.com
    username: elastic_user
    password: elastic_password
```

and
 
```yaml
settings:
  elasticsearch_url: http://elasticsearch.mygitlab.com
  elasticsearch_username: elastic_user
  elasticsearch_password: elastic_password
```
are exactly the same and match `elasticsearch_url`, `elasticsearch_username` and `elasticsearch_password` settings.
This means you can flexibly structure your configuration Yaml, where a map child keys are prefixed by parent key (here
`elasticsearch` parent key was a prefix for `url`, `username` and `password` keys). Simply:
 ```yaml
settings:
  prefix1:
    prefix2:
      value21: 'value21'
    value1: 'value1'
  prefix1_value2: 'value2'
```
will try to configure following properties: `prefix_value1`, `prefix_value2` and `prefix1_prefix2_value21`.
 You only need to follow available [Application Settings](https://docs.gitlab.com/12.4/ee/api/settings.html).

**Note:** Any invalid keys will be discarded, warn message will be presented, but _GCasC_ will continue execution.

You can adjust your Yamls by splitting them into multiple or injecting environment variables into certain values using
`!include` or `!env` directives respectively. Example is shown below:

```yaml
settings:
  elasticsearch: !include config/elasticseach.yml
  terms: !include tos.md
```

where:

* `settings.elasticsearch` is injected from file under `./config/elasticsearch.yml` path. Its configuration may look
like this:
    ```yaml
    url: http://elasticsearch.mygitlab.com
    username: !env ELASTICSEARCH_USERNAME
    password: !env ELASTICSEARCH_PASSWORD
    ``` 
  Note that here also `ELASTICSEARCH_USERNAME`, `ELASTICSEARCH_PASSWORD` are used to inject username and password
  from environment variables
* `settings.terms` is injected from `./tos.md` file


