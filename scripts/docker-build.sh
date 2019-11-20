#!/bin/bash

rc=0
image_name=hoffmannlaroche/gcasc

dockerfile=./Dockerfile
project="GitLab Configuration as Code"
branch=${TRAVIS_BRANCH}
tag=${TRAVIS_TAG}
revision=${TRAVIS_COMMIT}

if [[ ! -f "$dockerfile" ]]; then
  echo "Dockerfile in path $dockerfile does not exist"
  exit 1
fi

build_docker_image() {
  echo "Building Docker image from branch: $branch"
  docker build \
    -f $dockerfile \
    --label project="$project" \
    --label branch="$branch" \
    --label revision="$revision" \
    --label license="Apache License 2.0" \
    --pull \
    --rm \
    -t $image_name \
    ./
  rc=$?
}

apply_tags() {
  tag_image=$1
  shift
  for tag in "$@"
  do
    echo "Tagging $image_name with $image_name:${tag}"
    docker tag $tag_image $image_name:${tag}
  done
}

prepare_tags() {
  if [[ "$branch" == "master" ]]; then
    apply_tags $image_name latest
  fi

  if [[ "$branch" == "$tag" ]]; then
    apply_tags $image_name latest-stable $tag
  fi
}

build_docker_image
prepare_tags

exit $rc