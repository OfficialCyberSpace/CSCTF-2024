#!/bin/bash

export PATH=$PATH:/usr/local/bundle/bin
export BUNDLE_APP_CONFIG=/usr/local/bundle
export GEM_HOME=/usr/local/bundle

cd /home/user || exit
/usr/local/bundle/bin/rackup -E deployment -o 0.0.0.0 -p 1337