#!/bin/bash

cd .. 

# clear from git
find . -name '*.pyc' | xargs -n 1 git rm --cached

# clear from project
find . -name '*.pyc' -delete