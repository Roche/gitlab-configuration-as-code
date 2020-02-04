# Appearance

_GCasC_ allows configuring instance Appearance. Appearance can be configured either through UI (under Apperance in Admin Area)
or API. Using this you can apply branding to your GitLab instance and provide basic information to your users.

**Reference:** https://docs.gitlab.com/12.7/ee/api/appearance.html

Appearance structure is flexible. It starts with a root key `appearance`. Then you provide
configuration options as defined in [these docs](https://docs.gitlab.com/12.7/ee/api/appearance.html). For example

```yaml
appearance:
  title: "GitLab instance title"
  description: "Some description of GitLab instance"
  header:
    logo: "http://path-to-your-logo.com/logo.png"
    message: "This is message to show in header"
```

**Note:** Any invalid keys will be discarded, warn message will be presented, but _GCasC_ will continue execution.