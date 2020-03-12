# Instance Feature Flag

GitLab comes with some functionality configurable using feature flags. Part of the GitLab functionality is turned
off, where to enable it you need to use API, cause it does not offer UI for setting up feature flags. 

**Reference:** https://docs.gitlab.com/ee/api/features.html

**Important!** This is authoritative configuration, thus any existing Feature Flags will be removed
and replaced with the ones defined in config file. If none are defined in config file, existing Feature Flags
will remain untouched.

Features offered by GitLab are not collected in a single documentation page, but they are scattered. Please
reference to GitLab documentation for them.
Features yaml structure starts with a root key `features` . It's structure is defined below:

```yaml
features: [list]
  - name: [string]
    value: [bool/int]
    feature_group: [string|optional]
    canaries: [list|optional]
      - user: [string|optional]
        group: [string|optional]
        project: [string|optional]
```

To configure certain feature for a limited set of users, you can specify `canaries`. It allows configuring
features per user, group or project.

Example of complex features configuration:
```yaml
features:
  - name: some_percentage_feature
    value: 25
    canaries: 
      - user: user1
      - user: user2
  - name: some_percentage_feature
    value: 50
    canaries: 
      - user: myuser
        group: mygroup
        project: mygroup1/myproject
      - project: mygroup1/myproject2
```

It will configure `some_percentage_feature` with value `25` for users `user1` and `user2`, while
with value `50` for user `myuser`, group `mygroup` and projects `mygroup1/myproject`, `mygroup1/myproject2`. 