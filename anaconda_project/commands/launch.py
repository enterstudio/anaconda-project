# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Copyright © 2016, Continuum Analytics, Inc. All rights reserved.
#
# The full license is in the file LICENSE.txt, distributed with this software.
# ----------------------------------------------------------------------------
"""The ``launch`` command executes a project, by default without asking questions (fails on missing config)."""
from __future__ import absolute_import, print_function

import sys

from anaconda_project.commands.prepare_with_mode import prepare_with_ui_mode_printing_errors
from anaconda_project.project import Project


def launch_command(project_dir, ui_mode, conda_environment, command, extra_command_args):
    """Run the project.

    Returns:
        Does not return if successful.
    """
    project = Project(project_dir, default_conda_environment=conda_environment, default_command=command)
    result = prepare_with_ui_mode_printing_errors(project, ui_mode=ui_mode, extra_command_args=extra_command_args)

    if result.failed:
        return
    elif result.command_exec_info is None:
        print("No known launch command for project %s; try adding a 'commands:' section to project.yml" % project_dir,
              file=sys.stderr)
    else:
        try:
            result.command_exec_info.execvpe()
        except OSError as e:
            print("Failed to execute '%s': %s" % (" ".join(result.command_exec_info.args), e.strerror), file=sys.stderr)


def main(args):
    """Start the launch command and return exit status code.."""
    # I don't understand why argparse does this to us and leaves the '--' in, but whatever.
    if args.extra_args_for_command and args.extra_args_for_command[0] == '--':
        args.extra_args_for_command = args.extra_args_for_command[1:]
    launch_command(args.project, args.mode, args.environment, args.command, args.extra_args_for_command)
    # if we returned, we failed to launch the command and should have printed an error
    return 1
