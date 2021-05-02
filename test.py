from unittest import TestLoader, TextTestRunner
from coverage import Coverage

if __name__ == '__main__':
    cov = Coverage()
    cov.start()
    tests = TestLoader().discover('test', pattern='test*.py')
    result = TextTestRunner(verbosity=2).run(tests)
    cov.stop()
    cov.report(include='*pool_*.py')
