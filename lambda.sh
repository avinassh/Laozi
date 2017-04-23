find . -name '*.pyc' -delete
rm -rf __pycache__
pip install -r requirements.txt -t .
zip -r lambda.zip *
git clean -f -d