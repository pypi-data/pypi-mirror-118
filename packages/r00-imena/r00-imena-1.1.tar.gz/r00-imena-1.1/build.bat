cd i:\projects\packages\imena-package\
python setup.py sdist
pip uninstall -y r00-imena
twine upload -u r00ft1h -p %M9Y*x@CBiys2e8t --verbose dist/*
pip install r00-imena
pause