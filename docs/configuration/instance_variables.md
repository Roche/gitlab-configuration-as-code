# Instance CI/CD Variables

_GCasC_ allows configuring CI/CD Instance Variables. Instance variables 
are useful for no longer needing to manually enter the same credentials 
repeatedly for all your projects. Instance-level variables are 
available to all projects and groups on the instance.

**Reference:** https://docs.gitlab.com/ee/api/instance_level_ci_variables.html

## Properties

Instance variables configuration starts with a root key `instance_variables`. 
Then you can either define
1. simple _key-value_ property, where _key_ is a name of variable and 
   _value_ is its value.
2. complex property to provide additional variables configuration.
   Property _key_ is a name of variables

Key must be one line, using only letters, numbers, or _ (underscore), with no spaces.

| **Property**                                 | **Description**                                                                               | **Default** |
|----------------------------------------------|-----------------------------------------------------------------------------------------------|-------------|
| `instance_variables.<var_key>.value`         | Value of the instance variable                                                                |             |
| `instance_variables.<var_key>.protected`     | If `true`, the variable is only available in pipelines that run on protected branches or tags | `false`     | 
| `instance_variables.<var_key>.masked`        | If `true`, variable value is masked in jobs' logs. Value to be masked needs to follow [these requirements](https://docs.gitlab.com/ee/ci/variables/#masked-variable-requirements) | `false`    |
| `instance_variables.<var_key>.variable_type` | Type of the variable. Needs to be one of `env_var`, `file`                                    | `env_var`   |

**Note:** You can reference variables in other variables, e.g. you can set
`MY_VARIABLE: 'the other variable is $OTHER_VARIABLE`.

## Example 

```yaml
instance_variables:
  MY_VARIABLE: 'value of my instance variable'
  ANOTHER_VARIABLE:
    value: !env SOME_PASSWORD
    masked: true
    protected: false
  SOME_FILE_VARIABLE:
    value: |
      long file data
    variable_type: file
```
