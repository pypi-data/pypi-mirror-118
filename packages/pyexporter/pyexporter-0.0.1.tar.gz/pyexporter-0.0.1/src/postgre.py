#!/usr/bin/env python3
# -*- coding: utf-8 -*-
''' Class for work with testing Modules '''

import os
import sys
import time
import psycopg2

class Postgre():
  ''' Class for work with DB '''

  def __init__ (self, config, verbose):
    """ Initialising object
    Parameters
    ----------
    config : dict
        config of module
    verbose : bool
        verbose output
    """
    self.config = config
    self.verbose = verbose
    self.handle = None
    self.host = '127.0.0.1'
    self.port = 0
    self.dbName = ''
    self.user = ''
    self.password = ''

    if 'host' in self.config:
      self.host = self.config['host']
    if 'port' in self.config:
      self.port = int(self.config['port'])
    if 'name' in self.config:
      self.dbName = self.config['name']
    if 'user' in self.config:
      self.user = self.config['user']
    if 'password' in self.config:
      self.password = self.config['password']

    self.url = "pg://%s@%s:%d/%s" % (self.user, self.host, self.port, self.dbName)
  
  def close(self):
    if not self.handle is None:
      if hasattr(self.handle, 'close') and callable(getattr(self.handle, 'close')):
        self.handle.close()
    self.handle = None

  def reconnect(self):
    self.close()

    timeout = 15
    stop_time = 1
    elapsed_time = 0
    str_err = ''
    while (self.handle is None) and elapsed_time < timeout:
      time.sleep(stop_time)
      elapsed_time += stop_time
      try:
        self.handle = psycopg2.connect(host=self.host,
                                        port=self.port,
                                        user=self.user,
                                        password=self.password,
                                        dbname=self.dbName)
          
      except Exception as e:
        if self.verbose:
          print("DBG: WAIT: %d: Connect to PostgreSQL '%s':%s" % (elapsed_time, self.url, str(e)))
        str_err = str(e)

    if self.handle is None:
      print("FATAL: Connect to PostgreSQL '%s': %s" % (self.url, str_err))
      return None    
    
    if self.verbose:
      print("DBG: Connected to PostgreSQL '%s'" % (self.url))
    return self.handle
    
  def insertData(self, columns, data):
    cnt = 0
    unique_field = 'id'
    if 'unique_field' in self.config:
      unique_field = self.config['unique_field']
    table = 'tablename'
    if 'table' in self.config:
      table = self.config['table']
      

    mapsfields = {}
    for _, name in columns.items():
      if 'fields' in self.config:
        for field, fieldprop in self.config['fields'].items():
          if ('field' in fieldprop) and name == fieldprop['field']:
            mapsfields[name] = field
          else:
            if name == field:
              mapsfields[name] = field
      else:
        mapsfields[name] = name

    try:
      cursor = self.handle.cursor()
      for record in data:
        sql = self.makeSQLIU(table, unique_field, columns, mapsfields, record)
        if self.verbose:
          print("DBG: SQL: %s" % sql)
        cursor.execute(sql)
        if cnt % 100 == 0:
          self.handle.commit()

        cnt = cnt + 1
      self.handle.commit()
    except Exception as e:
      print("FATAL: insertData DB '%s': %s" % (self.url, str(e)))
      return -1
    return cnt

  def getVal(self, key, value):
    if not 'fields' in self.config:
      return "'" + str(value) + "'"
    if not key in self.config['fields']:
      return "'" + str(value) + "'"
    if not 'type' in self.config['fields'][key]:
      return "'" + str(value) + "'"

    if 'int' == self.config['fields'][key]['type']:
      return str(value)

    if 'boolean' == self.config['fields'][key]['type']:
      v = str(value).lower()
      if v == '1' or v == 'on' or v == 'true' or v == 'yes' or v == 'y':
        return 'TRUE'
      return 'FALSE'

    if 'strings' == self.config['fields'][key]['type']:
      arstr = value.split("\n")
      val = "'{"
      for i, s in enumerate(arstr):
        if i > 0:
          val = val + ','
        val = val + '"' + s + '"'
      val = val + "}'"
      return val
    
    return "'" + str(value) + "'"

  def makeSQLIU(self, table, unique_field, columns, mapsfields, record):
    insert_columns = ''
    insert_data = ''
    update_set = ''
    for _, name in columns.items():
      if not name in mapsfields:
        continue
      mapname = mapsfields[name]

      if len(insert_columns) > 0:
        insert_columns = insert_columns + ','
      insert_columns = insert_columns + mapname
      
      if len(insert_data) > 0:
        insert_data = insert_data + ','
      insert_data = insert_data + self.getVal(mapname, record[name])
      
      if len(update_set) > 0:
        update_set = update_set + ','
      update_set = update_set + mapname + '=' + self.getVal(mapname, record[name])

    return 'INSERT INTO ' + table + ' (' + insert_columns + ') VALUES (' + insert_data + ') ON CONFLICT (' + unique_field + ') DO UPDATE SET ' + update_set + ';'

