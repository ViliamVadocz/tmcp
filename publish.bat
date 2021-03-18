rmdir /s /q dist
mkdir dist
python setup.py sdist
twine upload dist/*
