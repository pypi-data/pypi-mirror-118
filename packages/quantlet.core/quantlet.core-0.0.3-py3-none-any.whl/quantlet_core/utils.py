#
#     QuantLET-core - Core componenents in QuantLET
#
#     Copyright (C) 2006 Jorge M. Faleiro Jr.
#
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU Affero General Public License as published
#     by the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU Affero General Public License for more details.
#
#     You should have received a copy of the GNU Affero General Public License
#     along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import errno
import glob
import os
import pkgutil
from os import path


def remove_files(path, mask):
    """
    remove all files in path matching mask
    """
    files = glob.glob(os.path.join(path, mask))
    for f in files:
        os.remove(f)


def mkdir_p(path):
    """
    equivalent to mkdid -p
    """
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def packages_of_module(package):
    for _, modname, ispkg in pkgutil.iter_modules(package):
        yield modname, ispkg


def is_function(f):
    return hasattr(f, "__call__")


def is_iterable(item):
    return hasattr(item, "__iter__")


def class_fqn(cls):
    """
    Fully qualified name of a class
    """
    return '.'.join([cls.__module__, cls.__name__])


def extract_contents(setup_file, readme="README.md"):
    """
    Extract contents of a README file, for use by a setup(long_description)
    """
    this_directory = path.abspath(path.dirname(setup_file))
    with open(path.join(this_directory, readme), encoding='utf-8') as f:
        return f.read()


def extract_description(readme):
    """
    Extracts description of a list of lines (originally from a readme
    file)
    """
    for line in readme.split('\n'):
        parts = line.split(' - ')
        if len(parts) == 2:
            return line.strip()


class UndoOnExcept(object):
    """
    Context manager to rollback single operations on exception
    """

    def __init__(self, rollback, suppress=False):
        self.rollback = rollback
        self.suppress = suppress

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is not None:
            self.rollback()
        return self.suppress


class AllowRaises(object):
    """
    Use in a with block to catch possible exceptions (i.e. delete
    only if exists, create only if doesnt exist, etc)
    """

    def __init__(self, *exceptions):
        self.exceptions = exceptions

    def __enter__(self):
        pass

    def __exit__(self, _type, value, _traceback):
        return isinstance(value, self.exceptions)


class AssertRaises(AllowRaises):
    def __exit__(self, _type, value, _traceback):
        if value is None:
            assert False, '%s should have been raised' % self.exceptions
        return isinstance(value, self.exceptions)
