#! /usr/bin/env python
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os
import sys
import tempfile
import shutil
from mozdownload.scraper import DailyScraper
import mozinstall

#tmpdir = tempfile.mkdtemp()
#print "temp dir: %S", tmpdir
#downloaddir = tmpdir
downloaddir = os.getcwd()

datadir = os.path.join(os.getcwd(), "addon", "data")

if sys.platform == 'win32':
  platform = 'win32'
  file_extension = '.zip'
elif sys.platform == 'darwin':
  platform = 'mac64'
  file_extension = '.dmg'
elif sys.platform.startswith('linux'):
  platform = 'linux-i686'
  file_extension = '.tar.bz2'
else:
  raise NotImplementedError('platform %s not supported' % sys.platform)

# Download latest build of B2G Desktop.

scraper_keywords = { 'application': 'b2g',
                     'platform': platform,
                     'locale': 'en-US',
                     'version': None,
                     'directory': downloaddir }
kwargs = scraper_keywords.copy()
if platform == "win32":
  kwargs.update({ 'windows_extension': '.zip' })

build = DailyScraper(**kwargs)
print "Initiating download B2G Desktop latest build..."
build.download()


# Install B2G Desktop to addon's data directory.

for file in os.listdir(downloaddir):
  if file.endswith(file_extension):
    installer = os.path.join(downloaddir, file)
    break

platformdir = os.path.join(datadir, platform)

mozinstall.install(installer, platformdir)


# Clean up.

#shutil.rmtree(tmpdir)
