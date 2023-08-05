#!/usr/bin/env python3
# -*- coding: utf-8 -*-
''' Class for work with Excel '''
import pylightxl as xl

class ExcelExport():
  ''' Class for Excel '''

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
    self.config = {}
    if 'excel' in config:
      self.config = config['excel']
    self.columns = {}
    self.row_column = 0
  
  def findColumns(self, xls):
    self.columns = {}
    find = False
    pos = 1
    if 'row_title' in self.config:
      pos = self.config['row_title']
    self.row_column = pos + 1
    for i, row in enumerate(xls.ws(ws = self.config['sheet']).rows, start=pos):
      if find:
        self.row_column = i
        break
      for j, col in enumerate(row):
        if col != '':
          sj = str(j)
          if 'fields' in self.config:
            if col in self.config['fields']:
              self.columns[sj] = col
              find = True
          else:
            self.columns[sj] = col
            find = True
    return self.columns, find

  def getColumns(self):
    return self.columns
  
  def run(self):
    # readxl returns a pylightxl database that holds all worksheets and its data
    try:
      xls = xl.readxl(fn = self.config['filename'])
    except Exception as e:
      print("FATAL: Excel '%s': %s" % (self.config['filename'], str(e)))
      return [], False
    c, ok = self.findColumns(xls)
    if not ok:
      print("FATAL: Excel '%s': columns not found" % (self.config['filename']))
      return [], False
    return self.receiveData(xls), True
  
  def receiveData(self, xls):
    pos = self.row_column
    if 'row_data' in self.config:
      pos = self.config['row_data']
    data = []
    # TODO
    # for i, row in enumerate(xls.ws(ws = self.config['sheet']).rows, start=pos):
    i = -1
    for row in xls.ws(ws = self.config['sheet']).rows:
      i = i + 1
      if i < pos:
        continue
      record = {}
      for col, title in self.columns.items():
        record[title] = row[int(col)]
      data.append(record)
    if self.verbose:
      print("DBG: Excel: %s: read records %d" % (self.config['filename'], len(data)))
    return data

