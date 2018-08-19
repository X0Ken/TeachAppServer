TeachAppServer

# Run
```
pip install -r requirements.txt
python -m server.app
```

# Test
run all tests
```
python -m server.test.runtests
```
run one tests
```
python -m server.test.runtests server.test.test_teacherjob.TestJob.test_add
```

# Code Style
import style
```
isort -rc -ns __init__.py --force-single-line-imports server/
```
line width 79