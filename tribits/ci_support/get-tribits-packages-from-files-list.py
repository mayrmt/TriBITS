#!/usr/bin/env python

# @HEADER
# ************************************************************************
#
#            TriBITS: Tribal Build, Integrate, and Test System
#                    Copyright 2013 Sandia Corporation
#
# Under the terms of Contract DE-AC04-94AL85000 with Sandia Corporation,
# the U.S. Government retains certain rights in this software.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
# 1. Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution.
#
# 3. Neither the name of the Corporation nor the names of the
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY SANDIA CORPORATION "AS IS" AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL SANDIA CORPORATION OR THE
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# ************************************************************************
# @HEADER

from TribitsPackageFilePathUtils import *


#
# Read in the commandline arguments
#

usageHelp = \
r"""get-tribits-packages-from-files-list.py --deps-xml-file=<DEPS_XML_FILE> --files-list-file=<FILES_LIST_FILE>

This script returns a comma-seprated list of all of the project's TriBITS SE
packages that must be directly tested for changes in the input list of files.
This may also include the special package name 'ALL_PACKAGES' which means that
at least one changed file (e.g. <projectDir>/CMakeLists.txt) should result in
having to test all of the TriBITS packages in the project.  The logic for
which files should trigger testing all packages can be specialized for the
project through the Python module <projectDir>/cmake/ProjectFileChange.py.

This script is used in continuous integration testing workflows involving
TriBITS projects.  For such a scenario, the list files can come from:

  git diff --name-only <upstream>..<branch-tip>  >  changed-files.txt

where <upstream> is the commit reference that the local branch was created
from and <branch-tip> is the tip of the local branch.
"""

from optparse import OptionParser

clp = OptionParser(usage=usageHelp)

clp.add_option(
  "--deps-xml-file", dest="depsXmlFile", type="string",
  help="File containing TriBITS-generated XML data-structure the listing of packages, dir names, dependencies, etc.")

clp.add_option(
  "--files-list-file", dest="filesListFile", type="string", default=None,
  help="File containing the list of modified files relative to project base directory, one file per line." )

(options, args) = clp.parse_args()

if not options.filesListFile:
  raise Exception("Error, the option --files-list-file=FILENAME must be set!")

filesList = readStrFromFile(options.filesListFile).splitlines()

trilinosDependencies = getProjectDependenciesFromXmlFile(options.depsXmlFile)

packagesList = getPackagesListFromFilePathsList(trilinosDependencies, filesList, True)

print ','.join(packagesList)
