"""
  Object wrapper around the database
"""
import setup
import MySQLdb
from datetime import datetime

class dbObject(object):
  _db = None

  def __init__(self):
    self._changed = []
    if not dbObject._db:
      dbObject._db = MySQLdb.connect(**setup.DB_CONFIG)
      c = dbObject._db.cursor()
      c.execute("SET autocommit=1")

  def execute(self, sql, *args):
    try:
      c = dbObject._db.cursor(MySQLdb.cursors.DictCursor)
      c.execute(sql, *args)
    except (AttributeError, MySQLdb.OperationalError):
      dbObject._db = MySQLdb.connect(**setup.DB_CONFIG)
      c = dbObject._db.cursor(MySQLdb.cursors.DictCursor)
      c.execute("SET autocommit=1")
      c.execute(sql, *args)
    return c

  def load(self, id):
    if id:
      c = self.execute("""SELECT * FROM {table} WHERE id = %s""".format(table=self.__class__.__name__.lower()), (id,))
    else:
      c = self.execute("""SELECT * FROM {table}""".format(table=self.__class__.__name__.lower()))
    res = c.fetchone()
    c.close()
    for var in res:
      setattr(self, var, res[var])

  def commit(self):
    pass

  def loadFromQuery(self, query):
    c = self.execute(query)
    res = c.fetchone()
    c.close()
    for var in res:
      setattr(self, var, res[var])

  def loadFromDict(self, vars):
    for var in vars:
      setattr(self, var, vars[var])

  def loadAll(self):
    table = self.__class__.__name__.lower()
    result = []
    c = self.execute("""SELECT * FROM {table} ORDER BY id""".format(table=table))
    res = c.fetchone()
    while res:
      inst = self.__class__()
      inst.loadFromDict(res)
      result.append(inst)
      res = c.fetchone()
    c.close()
    return result

  def save(self):
    if not len(self._changed):
      return
    vals = []
    query = "UPDATE {table} SET ".format(table=self.__class__.__name__.lower())
    values = ""
    first = False
    for var in self.__dict__:
      if var[0] == '_':
        continue
      if var in self._changed:
        if first:
          query = query + ','
        else:
          first = True
        query = query + " {field} = %s".format(field=var)
        vals.append(self.__dict__[var])
    if 'id' in self.__dict__:
      query = query + " WHERE id = %s"
      vals.append(self.id)
    c = self.execute(query, vals)
    self.commit()
    self._changed = []
    c.close()

  def status(self):
    if 'id' in self.__dict__:
      self.load(id)
    else:
      self.load(False)
    return self.__dict__

if __name__ == '__main__':
  c = dbObject()
  curs = c.execute('SELECT * FROM config')
  row = curs.fetchone()
  curs.close
  print row

