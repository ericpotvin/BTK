# Bash ToolKit

Unittests and Code Coverage for Bash Script (inspired by shcov and shunit2).

This package contains:
- btkut: perform UnitTests
- btkcc: generate code coverage

# Install

### build RPM
**Before making any changes, make sure you update the "Release" target in the .spec file.**

First, create .tar.gz:
```
cd /path/to/build/SOURCE
tar czf btk.tar.gz btk/
```
And build the rpm file
```
cd /path/to/build/
rpmbuild --define "_topdir $(pwd)" -ba SPECS/btk.spec
```

### Install RPM
```
$ sudo rpm -ivh BTK-1-0.0.noarch.rpm
```

# Usage

### btkut
To run tests, add this at the end of the file of your *script_test.sh*
```
. btkut
```

#### Example
```
#!/bin/bash

function_x_test()
{
    # some tests
    assertTrue "$?"
}

. btkut
```

### btkcc
To generate the code coverage report, we need first to generate the data.
```
$ btkcc bash_script.sh
```

Then, generate the report
```
$ btkcc --report
```

This will generate a report that can be open via this URL:
```
file:///tmp/btk/report/index.html
```