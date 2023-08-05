"""
Command Line tool for the PeakRDL Python
"""

#!/usr/bin/env python3
import argparse
import os
import subprocess
import unittest.loader
from typing import List, Union

import coverage

from systemrdl import RDLCompiler
from systemrdl.node import Node, AddrmapNode

from peakrdl.python.exporter import PythonExporter


def build_command_line_parser() -> argparse.ArgumentParser:
    """
    generates the command line argument parser to be used by the module.

    Returns:
        command line args parser
    """
    parser = argparse.ArgumentParser(
        description='Generate Python output from systemRDL')
    parser.add_argument('infile', metavar='file', type=str,
                        help='input systemRDL file')

    parser.add_argument('--include_dir', type=str, action='append',
                        metavar='dir',
                        help='add dir to include search path')
    parser.add_argument('--outdir', type=str, default='.',
                        help='output director (default: %(default)s)')
    parser.add_argument('--top', type=str,
                        help='specify top level addrmap (default operation will use last defined '
                             'global addrmap)')
    parser.add_argument('--verbose', '-v', action='count', default=0,
                        help='set logging verbosity')
    parser.add_argument('--autoformat', action='store_true',
                        help='use autopep8 on generated code')

    checker = parser.add_argument_group('post-generate checks')
    checker.add_argument('--lint', action='store_true',
                         help='run pylint on the generated python')
    checker.add_argument('--test', action='store_true',
                         help='run unittests for the created')
    checker.add_argument('--coverage', action='store_true',
                         help='run a coverage report on the unittests')
    checker.add_argument('--html_coverage_out',
                         help='output director (default: %(default)s)')

    return parser


def compile_rdl(infile:str,
                incl_search_paths:Union[type(None), List[str]]=None,
                top:Union[type(None), str]=None) -> AddrmapNode:
    """
    Compile the systemRDL

    Args:
        infile: top level systemRDL file
        incl_search_paths: list of additional paths where dependent systemRDL files can be
            retrived from. Set to ```none``` if no additional paths are required.
        top: name of the top level address map

    Returns:

    """
    rdlc = RDLCompiler()
    rdlc.compile_file(infile, incl_search_paths=incl_search_paths)
    return rdlc.elaborate(top_def_name=top).top


def generate(root:Node, outdir:str, autoformatoutputs:bool=True) -> List[str]:
    """
    Generate a PeakRDL output package from compiled systemRDL

    Args:
        root: node in the systemRDL from which the code should be generated
        outdir: directory to store the result in
        autoformatoutputs: If set to True the code will be run through autopep8 to
                clean it up. This can slow down large jobs or mask problems

    Returns:
        List of strings with the module names generated

    """
    print('Info: Generating python for {} in {}'.format(root.inst_name, outdir))
    modules = PythonExporter().export(root, outdir,
                                      autoformatoutputs=autoformatoutputs)

    return modules

def run_lint(root, outdir):
    """
    Run the lint checks using pylint on a directory

    Args:
        root: name of the generated package (directory)
        outdir: location where the package has been written

    Returns:

    """
    subprocess.run(['pylint', '--rcfile',
                    os.path.join('tests','pylint.rc'),
                    os.path.join(outdir, root)],
                   check=False)

def main_function():
    """
    Main function for the Command Line tool, this needs to be separated out so that it can be
    referenced in setup.py

    Returns:
        None

    """

    cli_parser = build_command_line_parser()
    args = cli_parser.parse_args()

    print('***************************************************************')
    print('* Compile the SystemRDL                                       *')
    print('***************************************************************')
    spec = compile_rdl(args.infile, incl_search_paths=args.include_dir,
                       top=args.top)

    print('***************************************************************')
    print('* Generate the Python Package                                 *')
    print('***************************************************************')
    generate(spec, args.outdir, args.autoformat)

    if args.lint:
        print('***************************************************************')
        print('* Lint Checks                                                 *')
        print('***************************************************************')
        run_lint(outdir=args.outdir, root=spec.inst_name)
    if args.test:
        print('***************************************************************')
        print('* Unit Test Run                                               *')
        print('***************************************************************')
        if args.coverage:
            cov = coverage.Coverage(
                include=[f'*\\{spec.inst_name}\\reg_model\\*.py',
                         f'*\\{spec.inst_name}\\tests\\*.py'])
            cov.start()
        tests = unittest.TestLoader().discover(
            start_dir=os.path.join(args.outdir, spec.inst_name, 'tests'),
            top_level_dir=args.outdir)
        runner = unittest.TextTestRunner()
        runner.run(tests)

        if args.coverage:
            cov.stop()

        if args.html_coverage_out is not None:
            cov.html_report(directory=args.html_coverage_out)


if __name__ == '__main__':
    main_function()
