#!/usr/bin/env python3
# -*- coding: utf-8 -*-
''' Class for work with exporting data '''

import os
import sys
import time
import yaml

from .dirs import DirsExport
from .xls import ExcelExport
from .postgre import Postgre

class Exporter(object):
  ''' Class for load environment '''

  def __init__ (self, pathModules, pathTmp = '', verbose = True):
    """ Initialising object
    Parameters
    ----------
    pathModules : str
        path to modules settings
    pathTmp : str
        path to temporary files
    verbose : bool
        verbose output
    """
    self.verbose = verbose
    self.pathModules = os.path.abspath(pathModules)
    self.pathTmp = pathTmp
    if self.pathTmp == '':
      self.pathTmp = os.path.join(os.getcwd(), 'tmp')
    os.makedirs(self.pathTmp, exist_ok=True)
    self.modules = dict()
    self.operations = {
        'rsync': self._rsync,
        'excel2db': self._excel2db,
      }

  
  def scan(self):
    """ Scan subfolders for modules
    """
    if self.verbose:
      print("DBG: scan folder: %s" % self.pathModules)
      
    for r, d, f in os.walk(self.pathModules):
      for fileName in f:
        if '.yaml' in fileName:
          if self.verbose:
            print("DBG: load file: %s" % fileName)
          fullPath = os.path.join(self.pathModules, fileName)
          with open(os.path.join(fullPath), 'r') as stream:
            try:
              config = yaml.safe_load(stream)
              if 'name' in config:
                if self.verbose:
                  print("DBG: find export: %s" % config['name'])
                name = config['name']
                config['mod_path'] = fullPath
                if not 'actions' in config:
                  seq = ['rsync', 'excel2db']
                if not 'order' in config:
                  config['order'] = 0
                else:
                  config['order'] = int(config['order'])
                self.modules[name] = set()
                self.modules[name] = dict(sorted(config.items()))
              else:
                if self.verbose:
                  print("WRN: Export not found in %s" % fullPath)
            except yaml.YAMLError as exc:
              print("ERR: Bad format in %s: %s" % (fullPath, exc))

  def printList(self):
    """ Output the list of modules
    """
    for s in sorted(self.modules.items(), key=lambda k_v: k_v[1]['order']):
      print("LOG: Export: %s \t (order=%d)" % (s[1]['name'], s[1]['order']))

  def count(self):
    """ Count of modules
    """
    return len(self.modules)

  def getConfig(self, moduleName):
    """ Get configuration of module
        Parameters
        ----------
        moduleName : str
            name of module
    """
    return self.modules.get(moduleName, {})

  def getTmpFolder(self, moduleName):
    """ Get temporary path for module
        Parameters
        ----------
        moduleName : str
            name of the module
            
        Returns
        -------
        path:
            temporary path for the module
    """
    return os.path.join(self.pathTmp, moduleName)


  def _rsync(self, config):
    if 'rsync' in config:
      d = DirsExport(config, self.verbose)
      d.run()
      return True
    return False

  def _excel2db(self, config):
    if 'excel' in config:
      e = ExcelExport(config, self.verbose)
      data, ok = e.run()
      if ok:
        pg = Postgre(config['db'], self.verbose)
        pg.reconnect()
        pg.insertData(e.getColumns(), data)
        return True
    return False

  def runAll(self):
    for s in sorted(self.modules.items(), key=lambda k_v: k_v[1]['order']):
      self._runActions(s[1])

  def run(self, moduleName):
    result = False
    for s in self.modules.items():
      if moduleName == s[1]['name']:
        result = self._runActions(s[1])
        break
    return result

  def _runActions(self, config):
    result = False
    for s in config['actions']:
      if s in self.operations:
        if self.verbose:
          print("DBG: Export(%s) Action: %s" % (config['name'], s))
        result = self.operations[s](config)
        if not result:
          break
    return result
