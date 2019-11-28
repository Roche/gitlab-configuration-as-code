# Usage

## Docker image

Image is available in [Docker Hub](https://hub.docker.com/r/hoffmannlaroche/gcasc).

_GCasC_ Docker image working directory is `/workspace`. Thus you can quickly launch `gcasc` with:
```bash
docker run -v $(pwd):/workspace hoffmannlaroche/gcasc
```
It will try to find both GitLab client configuration and GitLab configuration in `/workspace` directory. You can modify
the behavior by passing environment variables:
* `GITLAB_CLIENT_CONFIG_FILE` to provide path to GitLab client configuration file
* `GITLAB_CONFIG_FILE` to provide a path to GitLab configuration file

```bash
docker run 
    -e GITLAB_CLIENT_CONFIG_FILE=/gitlab/client.cfg 
    -e GITLAB_CONFIG_FILE=/gitlab/config.yml 
    -v $(pwd):/gitlab
    hoffmannlaroche/gcasc
```

You can also configure a GitLab client using environment variables. More details about the configuration of 
GitLab client is [here](client.md).


## CLI


