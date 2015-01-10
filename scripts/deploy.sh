#!/bin/bash
#
set -ue

PROJECT=sauer-cloud

GIT_CLEAN_VERSION=$(git log -1 --pretty=format:%H)
GIT_VERSION="$GIT_CLEAN_VERSION"
if [ -n "$(git status --porcelain)" ]
then
  GIT_VERSION="dirty-$GIT_CLEAN_VERSION"
fi

function get_version() {
  local version
  version="$GIT_VERSION"

  while [ $# -gt 0 ]
  do
    if [ "$1" == "--version" ]
    then
      shift
      version=$1
    elif [ "${1/=*/}" == "--version" ]
    then
      version=${1/--version=/}
    fi
    shift
  done
  echo $version
}


echo -e "\n*** CHECKING GIT STATUS ***\n"
git status
echo
echo -e "Hit [ENTER] to continue: \c"
read


SCRIPTS_DIR=$( dirname $0 )
ROOT_DIR=$( dirname $SCRIPTS_DIR )

VERSION=$(get_version $*)
echo
echo "Deploying:"
echo " - version: $VERSION"
echo " - project: $PROJECT"

echo
echo "Deployed versions can be managed from the Developer Console:"
echo
echo "  https://console.developers.google.com/project/${PROJECT}/appengine/versions"


echo -e "\n*** CANCELLING ANY PENDING DEPLOYMENTS (just in case) ***\n"
gcloud --project $PROJECT preview app modules cancel-deployment --version $VERSION --project $PROJECT default $*


echo -e "\n*** DEPLOYING ***\n"
gcloud --project $PROJECT preview app deploy --version $VERSION --project $PROJECT $* .


echo -e "\n*** SETTING DEFAULT VERSION ***\n"
if [ "$VERSION" == "$GIT_CLEAN_VERSION" ]
then
  gcloud --project $PROJECT preview app modules set-default --version $VERSION --project $PROJECT default $*
else
  echo "WARNING: Default version update skipped due to version '$VERSION' != '$GIT_CLEAN_VERSION'"
  echo
fi
