# Environment variable readme
# https://docs.gitlab.com/ee/ci/variables/

# Predefined environment variables
# https://docs.gitlab.com/ee/ci/variables/predefined_variables.html

# Using docker images
# https://docs.gitlab.com/ee/ci/docker/using_REGISTRY_images.html

# .gitlab-ci.yml reference
# https://docs.gitlab.com/ee/ci/yaml/

# Container registry reference (authenticating, etc.)
# https://gitlab.com/help/user/packages/container_registry/index

variables:
  DOCKER_AUTH_CONFIG: '{ "auths":{ "https://apps.smartanalytics.io:23500": { "auth": "$REGISTRY_AUTH_HASH" } }}'

stages:
  - build
  - deploy

docker-build-master:
  image: apps.smartanalytics.io:23500/tmaier/docker-compose:latest
  stage: build

  services:
    - apps.smartanalytics.io:23500/docker:dind

  before_script:
    - docker login -u "$REGISTRY_LOGIN" -p "$REGISTRY_PASSWORD" $REGISTRY_URL

  script:
    - echo "|---- start build ----:>"
    - docker-compose -f docker-compose-prod.yml build --force-rm
    - docker-compose -f docker-compose-prod.yml push
    - echo ":>----  finish build ----=|"

  after_script:
    - docker logout $REGISTRY_URL

  only:
    - master
docker-deploy-master:
  image: apps.smartanalytics.io:23500/tmaier/docker-compose:latest
  stage: deploy

  before_script:
    - docker login -u "$REGISTRY_LOGIN" -p "$REGISTRY_PASSWORD" $REGISTRY_URL

  services:
    - apps.smartanalytics.io:23500/docker:dind

  script:
    - echo "|---- Start deploy ----:>"
    - docker stack deploy --with-registry-auth --compose-file=docker-compose-prod.yml {{params['project_name'] }} --prune
    - echo ":>---- Finish deploy ----=|"

  after_script:
    - docker logout $REGISTRY_URL

  only:
    - master
