#!/bin/bash
#
set -ue

gcloud preview app run \
  --host localhost \
  --admin-host localhost \
  . $*
