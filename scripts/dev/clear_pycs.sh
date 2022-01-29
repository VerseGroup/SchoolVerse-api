#!/bin/bash

# clear from git
cd .. 
cd .. 
find . -name '*.pyc' | xargs -n 1 git rm --cached

# clear from project
find . -name '*.pyc' -delete