cd i:\projects\packages\imena-package\
python setup.py sdist
pip uninstall -y imena
twine upload -u r00ft1h -p %M9Y*x@CBiys2e8t --verbose dist/*
pip install r00-imena
REM python setup.py sdist & pip uninstall -y imena & pip install  "I:\projects\packages\imena-package\dist\imena-1.0.tar.gz"