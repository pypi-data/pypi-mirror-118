#!/usr/bin/env python3
# -*- coding: utf-8 -*-
''' Class for work with RSync files '''
import sysrsync


class DirsExport():
  ''' Class for Sync files inside folders '''

  def __init__ (self, config, verbose):
    """ Initialising object
    Parameters
    ----------
    config : dict
        config of module
    verbose : bool
        verbose output
    """
    self.verbose = verbose
    self.config = None
    if 'rsync' in config:
      self.config = config['rsync']
  
  def run(self):
    if self.config and 'src' in self.config and 'dest' in self.config:
      options = ['-a']
      if self.verbose:
        print("DBG: RSYNC: '%s' => '%s'" % (self.config['src'], self.config['dest']))
        options.append('-v')
      sysrsync.run(source = self.config['src'],
                   destination = self.config['dest'],
                   sync_source_contents = True,
                   exclusions = ['.~*', 'Thumbs.db:encryptable'],
                   options = options,
                   verbose = self.verbose)
      return True
    return False

