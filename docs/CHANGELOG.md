## [0.2.0-dev.2](https://github.com/CrackingShells/Wobble/compare/v0.2.0-dev.1...v0.2.0-dev.2) (2025-09-15)


### Features

* add dataclass architecture for test results ([5fa1983](https://github.com/CrackingShells/Wobble/commit/5fa1983f02016462e687dd246b69f39629b57e5f))
* add positional path argument support to CLI ([5d3a6b2](https://github.com/CrackingShells/Wobble/commit/5d3a6b2180664e6b76690a6cd78f7b5d3620821f))
* enhance _ErrorHolder error messages with actionable details ([1a4ea48](https://github.com/CrackingShells/Wobble/commit/1a4ea486fcd156aef75ffae20bc9537da1f72e57))
* implement EnhancedOutputFormatter with observer integration ([510f016](https://github.com/CrackingShells/Wobble/commit/510f0166a1b0754471409db00326526546f7a81e))
* implement functional file output for discovery mode ([143bc6d](https://github.com/CrackingShells/Wobble/commit/143bc6d3b9d11032560b7241af3800b9b674fd51))
* implement Observer + Strategy pattern architecture ([c5d767d](https://github.com/CrackingShells/Wobble/commit/c5d767d5a265de9ec8f2521cb12d40c2c448feb4))
* implement resolved CLI argument system for file output ([087cc64](https://github.com/CrackingShells/Wobble/commit/087cc64285c932c089353616550d54411d00d87d))
* implement ThreadedFileWriter with ordered processing ([d2d1b9f](https://github.com/CrackingShells/Wobble/commit/d2d1b9f11e5a949f905ecffd58bb2055e075456e))
* integrate file output system with core test runner ([467b604](https://github.com/CrackingShells/Wobble/commit/467b6049873e3d00a1f807ed3b9306eff6bf4035))
* standardize Unicode symbol handling with ASCII fallback ([5431799](https://github.com/CrackingShells/Wobble/commit/5431799b48762546e025420f1c769fbd186961dd))


### Bug Fixes

* achieve 100% test pass rate - resolve final 3 test failures ([60a9af9](https://github.com/CrackingShells/Wobble/commit/60a9af9816f004fae1b7dd4d1d5ee4a7f67cbab3))
* handle unittest _ErrorHolder objects gracefully ([e8b5316](https://github.com/CrackingShells/Wobble/commit/e8b531643aa3e4520a47a1ca875b84a0b4b8e6b4))
* prevent duplicate output in file logging ([02f3b22](https://github.com/CrackingShells/Wobble/commit/02f3b2227a4a6c57aefd72a33a608ddbd56db730))
* resolve critical production issues in wobble framework ([1b2b526](https://github.com/CrackingShells/Wobble/commit/1b2b526d5348c712a00cd40171eb32c56dfbb613))
* resolve critical threading deadlock in file I/O system ([a4ddd9c](https://github.com/CrackingShells/Wobble/commit/a4ddd9cf4b73d8ced4d1b6bed0ddcc6241954148))
* resolve test compatibility issues for Python 3.12+ ([54a1da1](https://github.com/CrackingShells/Wobble/commit/54a1da1dc3b26ce7ec1d316a9d2f401e4db8b7a6))
* resolve threading deadlock in ThreadedFileWriter ([3751433](https://github.com/CrackingShells/Wobble/commit/3751433ae8f00dc9d79fff9580a4d7406070d865))


### Documentation

* add comprehensive file output section to CLI reference ([2ddc26b](https://github.com/CrackingShells/Wobble/commit/2ddc26b5ce3c38fb9e9affcc552e9809d557feaa))
* update documentation for file output feature across all guides ([80d1116](https://github.com/CrackingShells/Wobble/commit/80d11162c84a55d95b1f1156a332efd92381a091))


### Code Refactoring

* remove unused import in enhanced_output.py ([2108c3d](https://github.com/CrackingShells/Wobble/commit/2108c3d3114fa1e96fe686a9e819a3106097768c))
* standardize mock test class naming in enhanced output tests ([57fbb88](https://github.com/CrackingShells/Wobble/commit/57fbb88eac2206a7581592335028c87c8106fc38))

## [0.2.0-dev.1](https://github.com/CrackingShells/Wobble/compare/v0.1.0...v0.2.0-dev.1) (2025-09-10)


### Features

* convert template to wobble package structure ([f1705d8](https://github.com/CrackingShells/Wobble/commit/f1705d8ff9d42ece44f6a753422ce09de5ea74cc))
* implement core wobble framework functionality ([1b9f0a5](https://github.com/CrackingShells/Wobble/commit/1b9f0a5cf1119f85e0a33c4bcea4c0d708907344))


### Bug Fixes

* **ci deps:** `semantic-release-poetry-plugin` ([c8aefd6](https://github.com/CrackingShells/Wobble/commit/c8aefd6535f61583a37d5e4a1d40cacfe90c22f4))
* **ci:** remaining placeholder `{{PROJECT_NAME}}` ([9f8b833](https://github.com/CrackingShells/Wobble/commit/9f8b83390686b6d46de82570ff06388430e4cd61))
* remove duplicate CONTRIBUTING.md and update README ([c497654](https://github.com/CrackingShells/Wobble/commit/c4976543eb11eddec10c247f73be13d012d43269))
* resolve 11 test failures with implementation alignment ([6ee8399](https://github.com/CrackingShells/Wobble/commit/6ee8399f9983cbe9e883b5236f0f560c950876eb))
* resolve final test failure in test_timing_accuracy ([dbc667b](https://github.com/CrackingShells/Wobble/commit/dbc667bafe01f488d026f4d89e62cb633bf80845))


### Documentation

* add comprehensive developer documentation ([26609e9](https://github.com/CrackingShells/Wobble/commit/26609e99d10e69502adf88e8e2d68197744ee45e))
* add comprehensive user documentation ([bfae733](https://github.com/CrackingShells/Wobble/commit/bfae733f52cb5be9899fe167fb515c99d2714b0f))
* **fix:** inaccurate command reference ([db6b2e7](https://github.com/CrackingShells/Wobble/commit/db6b2e72ca848c6ed921a2aef1c11ec7e2a39a15))
