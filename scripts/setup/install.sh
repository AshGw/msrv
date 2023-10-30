#!/bin/bash

if [[ "$(uname -s)" == "MINGW"* ]]; then
  python.exe -m pip install --upgrade pip
else
  pip install --upgrade pip
fi
echo "installing project requirements"
pip install -r scripts/requires.txt
pip install -r scripts/dev_requires.txt
python setup.py develop
rm -rf app.egg-info
pre-commit install
cat <<EOF >> .git/hooks/pre-push
#!/bin/bash

echo "Before pushing, did you tie your shoes right ?"
echo "Running tests.."
pytest tests --no-header --no-summary -q

if [ \$? -ne 0 ]; then
  echo "Testing failed. Push aborted."
  exit 1
else
  printf "Testing went successful!\nPushing changes.."
fi

exit 0
EOF
printf  "pre-push installed\nDevelopment environment ready!"
