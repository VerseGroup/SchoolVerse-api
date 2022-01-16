cd .. 
cd .. 
find . -name '*.pyc' | xargs -n 1 git rm --cached
echo "cleared pycs"