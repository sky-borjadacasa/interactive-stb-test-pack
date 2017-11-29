# Test-pack

This is the project with the python code that will run the set-top-box tests.

## Writing tests

Tests should be put in the `tests` directory where they will be found by the
test-runner. The file `sky_plus_utils.py` has most of the needed utils to easily write more tests.

For more info go to:

* [stb-tester ONE manual](https://stb-tester.com/manual-stb-tester-one)
* [Python API](https://stb-tester.com/manual-stb-tester-one/python-api)
* [Using FrameObjects](https://stb-tester.com/tutorials/using-frame-objects-to-extract-information-from-the-screen)

## Remote-control configuration

Infrared remote control configuration belongs in the `config/remote-control/`
directory. See [configuration-files](https://stb-tester.com/manual-stb-tester-one/advanced-configuration#configuration-files) for details.

The **Sky Plus** remote was already added.

## Developing for the STB-Tester

**STB-Tester** software only works on Linux, so we need to use the `stbt-docker` command line util to check and debug our test code.

### Using `pylint`

`pylint` is used to check Python code. The way to call it through `stbt-docker` is:

```
./stbt-docker stbt lint tests/*.py
```
