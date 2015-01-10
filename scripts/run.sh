#!/bin/bash
#
set -ue

PROJECT=sauer-cloud

gcloud --project $PROJECT preview app run \
  --host localhost \
  --admin-host localhost \
  . $*
