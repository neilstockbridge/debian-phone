
import sqlite3
import re


db = sqlite3.connect('/tmp/debian-phone-test.sqlite3')
sql = db.cursor()


# A list of params for all invocations of "columns" before the class method was defined:
columns_params = []
def columns(*columns):
  columns_params.append( columns)

class MetaRecord(type):
  def __new__(cls, name, bases, dictionary):
    global columns_params
    Record = super(MetaRecord, cls).__new__(cls, name, bases, dictionary)
    for pr in columns_params:
        Record.columns( pr)
    columns_params = []
    return Record

class Model(object):

  __metaclass__ = MetaRecord

  @classmethod
  def columns( cls, columns):
    cls.columns = columns

  @classmethod
  def table_name( cls):
    return cls.__name__.lower()+"s"

  @classmethod
  def count( cls):
    sql.execute("SELECT COUNT(1) FROM %s"% cls.table_name())
    return sql.fetchone()[0]

  @classmethod
  def all( cls, order=None, select=None):
    select_columns = cls.columns if select is None else select.split(", ")
    order_sql = "" if order is None else " ORDER BY %s"% order
    query = "SELECT %s FROM %s%s" % ( ",".join(select_columns), cls.table_name(), order_sql )
    return [ cls.record_from( row, select_columns) for row in sql.execute( query)]

  @classmethod
  def find( cls, id):
    query = "SELECT %s FROM %s WHERE id = %s" % ( ",".join(cls.columns), cls.table_name(), id )
    return cls.record_from( sql.execute( query).fetchone(), cls.columns )

  def __init__( self, **kwargs):
    for cl in self.__class__.columns:
      self.__dict__[ cl] = kwargs[ cl] if cl in kwargs else None

  def is_new( self):
    return self.id is None

  def save( self):
    table_name = self.__class__.table_name()
    # NOTE: "[1:]" below assumes that the PK ("id") is the first column
    columns = self.__class__.columns[1:]
    if self.is_new():
      column_names = ",".join( columns)
      placeholders = ",".join( ["?"] * len( columns) )
      values = [ self.__dict__[cl] for cl in columns]
      stmt = "INSERT INTO %s ( %s) VALUES ( %s)" % ( table_name, column_names, placeholders )
      print "st", stmt
      print "vl", values
      sql.execute( stmt, values)
      # FIXME: set the automatically created id
    else:
      assignments = ",".join( ["%s = ?"% cl for cl in columns] )
      values = [ self.__dict__[cl] for cl in columns]
      stmt = "UPDATE %s SET %s WHERE id = ?" % ( table_name, assignments)
      sql.execute( stmt, values+[self.id])
    db.commit()

  def destroy( self):
    table_name = self.__class__.table_name()
    sql.execute( "DELETE FROM %s WHERE id = ?"% table_name, [self.id])
    db.commit()

  @classmethod
  def record_from( cls, row, columns):
    # Make a new record object to represent this record
    record = cls.__new__( cls)
    # Assign the values from the selected columns to attributes of the same name
    for i in range( 0, len( columns) ):
      column_name = columns[ i]
      value = row[ i]
      record.__dict__[ column_name] = value
    return record

#__all__ = [ActiveRecord, belongs_to]


class Contact( Model):
  columns("id", "name", "number")
  # TODO: Schema def should be here


class Event( Model):
  columns("id", "when_happened", "contact_id", "type", "outcome", "content")


#print Contact.count()
#contacts = Contact.all(order="name", select="name, number")
#for ct in contacts:
#  print ct.number

#neil = Contact.find( 1)
#print neil.name
#neil.name = "Neil2"
#neil.save()

#ct = Contact()
#ct.number = "111"
#ct.save()

#ct = Contact.find( 3)
#print ct.id
#ct.destroy()


# This is the definition of the schema.  It's a map from table name to table
# definition.  A table definition is a list of column definitions, which are
# strings of the form: "N: OP" where N in the name of the column and OP are the
# SQLite3 options.
#
tables = {
  "contacts": [
    "id:     integer primary key autoincrement not null",
    "name:   indexed text",
    "number: indexed text not null",
    ],
  "events": [
    "id:            integer primary key autoincrement not null",
    "when_happened: indexed datetime not null",
    "contact_id:    indexed integer",
    "type:          indexed text",
    "outcome:       text",
    "content:       text",
    ],
}

# Provides a list of DDL statements that create the given schema.  These may be
# emitted, sorted and then compared to a schema dump to see if the expected
# schema agrees with the actual schema.
#
def statements_to_create( tables):
  ddl = []
  indexes = []
  for table_name, columns in tables.iteritems():
    ddl_for_columns = []
    for column_def in columns:
      column_name, options = re.split(": +", column_def)
      if options.startswith("indexed "):
        options = options[8:]
        indexes.append('CREATE INDEX "%s_%s" ON "%s" ("%s");'% ( table_name, column_name, table_name, column_name) )
      ddl_for_columns.append('"%s" %s'% ( column_name, options) )
    ddl.append('CREATE TABLE "%s" (%s);'% ( table_name, ", ".join(ddl_for_columns)) )
  return ddl + indexes

#print "\n".join( statements_to_create(tables) )

#db.close()

