"""State-Sequence Grader."""


from ast import (Name, Load, Store,
                 Assign, Call, Constant, Lambda, Module,
                 fix_missing_locations, parse, unparse)
from collections.abc import Callable
from copy import deepcopy
from inspect import stack
import os
from pathlib import Path
from pprint import pprint
from shutil import copyfile
from tempfile import NamedTemporaryFile
from typing import Optional, Union

from codejail.safe_exec import safe_exec

from grader_support.gradelib import Grader
from grader_support.graderutil import change_directory
from grader_support.run import run


class StateSeqGrader(Grader):
    """State-Sequence Grader."""

    _GRADER_VAR_NAME: str = 'grader'

    _SUBMISSION_FILE_TEST_FUNC_VAR_NAME: str = '__SUBMISSION_FILE_TEST_FUNC__'
    _SUBMISSION_FILE_TEST_RESULT_VAR_NAME: str = '__SUBMISSION_FILE_TEST_RESULT__'   # noqa: E501

    _SUBMISSION_MODULE_NAME: str = '_submission'
    _SUBMISSION_MODULE_FILE_NAME: str = f'{_SUBMISSION_MODULE_NAME}.py'

    def __init__(self, _unsafe_func: Callable[[Union[str, Path]], bool], /):
        """Initialize State-Sequence Grader."""
        super().__init__()

        self.add_input_check(check=self.check_submission_str)

        if hasattr(self, 'set_only_check_input'):   # S4V customization
            self.set_only_check_input(value=True)

        # stackoverflow.com/a/56764010
        self.file_path: Path = Path(stack()[1].filename)

        with open(file=self.file_path,
                  mode='rt',
                  buffering=-1,
                  encoding='utf-8',
                  errors='strict',
                  newline=None,
                  closefd=True,
                  opener=None) as f:
            self.module: Module = parse(source=f.read(),
                                        filename=self.file_path,
                                        mode='exec',
                                        type_comments=False,
                                        feature_version=None)

            # REQUIRED assignment to variable named `grader`
            grader_assignment: Assign = next(i for i in self.module.body
                                             if isinstance(i, Assign) and
                                             i.targets[0].id == self._GRADER_VAR_NAME)  # noqa: E501

            # REQUIRED instantiation of StateSeqGrader class instance
            # with 1 single lambda positional argument
            assert isinstance(submission_file_test_func_code :=
                              grader_assignment.value.args[0], Lambda), \
                '*** SUBMISSION FILE TEST FUNC MUST BE A LAMBDA ***'

            self.module.body.append(
                Assign(targets=[Name(id=self._SUBMISSION_FILE_TEST_FUNC_VAR_NAME,   # noqa: E501
                                     ctx=Store())],
                       value=submission_file_test_func_code,
                       type_comment=None))

    def check_submission_str(self, submission_str: str, /) -> Optional[str]:
        """Test submission string."""
        with NamedTemporaryFile(mode='wt',
                                buffering=-1,
                                encoding='utf-8',
                                newline=None,
                                suffix=None,
                                prefix=None,
                                dir=None,
                                delete=False,
                                errors='strict') as f:
            f.write(submission_str)

        _module: Module = deepcopy(self.module)
        _module.body.append(
            Assign(targets=[Name(id=self._SUBMISSION_FILE_TEST_RESULT_VAR_NAME,
                                 ctx=Store())],
                   value=Call(func=Name(id=self._SUBMISSION_FILE_TEST_FUNC_VAR_NAME,   # noqa: E501
                                        ctx=Load()),
                              args=[Constant(value=f.name)],
                              keywords=[],
                              starargs=[],
                              kwargs=[]),
                   type_comment=None))

        try:
            safe_exec(code=unparse(ast_obj=fix_missing_locations(node=_module)),   # noqa: E501
                      globals_dict=globals(),
                      files=None,
                      python_path=None,
                      limit_overrides_context=None,
                      slug=None,
                      extra_files=None)

        except Exception as err:   # pylint: disable=broad-except
            complaint_str: str = str(err)

        finally:
            os.remove(path=f.name)

        complaint_str: Optional[str] = (
            None
            if globals()[self._SUBMISSION_FILE_TEST_RESULT_VAR_NAME]
            else '*** INCORRECT ***')

        return complaint_str

    def __call__(self, submission_file_path: Union[str, Path], /,
                 *, submission_only: bool = False):
        """Run State-Sequence Grader."""
        with change_directory(self.file_path.parent):
            copyfile(src=submission_file_path,
                     dst=self._SUBMISSION_MODULE_FILE_NAME,
                     follow_symlinks=True)

            # pylint: disable=import-outside-toplevel

            if submission_only:
                pprint(run(grader_name=self.file_path.stem,
                           submission_name=self._SUBMISSION_MODULE_NAME),
                       stream=None,
                       indent=2,
                       width=80,
                       depth=None,
                       compact=False,
                       sort_dicts=False,
                       # underscore_numbers=True   # Py3.10+
                       )

            else:
                from xqueue_watcher.jailedgrader import main

                main(args=(self.file_path.name,
                           self._SUBMISSION_MODULE_FILE_NAME))

            os.remove(path=self._SUBMISSION_MODULE_FILE_NAME)