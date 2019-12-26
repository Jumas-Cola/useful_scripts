@echo on
cmd /k "py -3.7 -m venv env & cd /d env\Scripts & activate & cd /d ..\..\ & pip install -r requirements.txt & exit"