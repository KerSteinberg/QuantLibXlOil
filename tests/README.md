# Unit Test Suite

This folder contains test cases for the project code.

We use `pytest` as test framework.

## Test File Names

Test file names are of the form `test_sourcefilename.py`.

Here, `test_` is a fixed and common prefix. The part `sourcefilename` mirrors the file name of the source code being tested.

## Test Case Specification

Test cases are formulated for individual source functions.

Each test case is implemented by a function of the following form.

```
def test_qlFunctionName():
    import QuantLib as ql
    from quantlibxloil import qlFunctionName, ...
    ...
    assert ...
```

Function name prefix is `test_`. The part `qlFunctionName` corresponds to the name of the source function being tested.
 
