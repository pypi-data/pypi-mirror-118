cd i:\projects\packages\imena-package\
DEL /S /Q i:\projects\packages\imena-package\dist\
python setup.py sdist
pip uninstall -y r00-imena
REM Вручную выполнить
REM twine upload -u r00ft1h -p %M9Y*x@CBiys2e8t --verbose dist/*
REM pip install r00-imena==1.2
