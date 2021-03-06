#  _________________________________________________________________________
#
#  Pyomo: Python Optimization Modeling Objects
#  Copyright (c) 2014 Sandia Corporation.
#  Under the terms of Contract DE-AC04-94AL85000 with Sandia Corporation,
#  the U.S. Government retains certain rights in this software.
#  This software is distributed under the BSD License.
#  _________________________________________________________________________

import sys
import copy

try:
    import pkg_resources
    #
    # Load modules associated with Plugins that are defined in
    # EGG files.
    #
    for entrypoint in pkg_resources.iter_entry_points('pyomo.command'):
        plugin_class = entrypoint.load()
except Exception:
    err = sys.exc_info()[1]
    sys.stderr.write( "Error loading pyomo.command entry points: %s  entrypoint='%s'\n" % (err, entrypoint) )


import pyomo.scripting.pyomo_parser


def main(args=None, get_return=False):
    #
    # Load subcommands
    #
    import pyomo.environ
    #
    # Parse the arguments
    #
    parser = pyomo.scripting.pyomo_parser.get_parser()
    if args is None:
        args = copy.copy(sys.argv[1:])
    #
    # This is a hack to convert a command-line to a 'solve' subcommand
    #
    if not args:
        args.append('-h')
    if args[0][0] == '-':
        if not args[0] in ['-h', '--help', '--version']:
            print("WARNING: converting to the 'pyomo solve' subcommand")
            args = ['solve'] + args[0:]
    elif not args[0] in pyomo.scripting.pyomo_parser.subparsers:
        print("WARNING: converting to the 'pyomo solve' subcommand")
        args = ['solve'] + args[0:]
    #
    # Process arguments
    #
    ret = parser.parse_known_args(args)
    #
    # Process the results
    #
    if ret[0].func.__code__.co_argcount == 1:
        #
        # If the execution function only accepts one argument, then we
        # create an exception if there are unparsed arguments.
        #
        if len(ret[1]) > 0:
            #
            # Re-parse the command-line to create an exception
            #
            parser.parse_args(args)
        retval = ret[0].func(ret[0])
    else:
        retval = ret[0].func(*ret)
    if get_return:
        return retval

