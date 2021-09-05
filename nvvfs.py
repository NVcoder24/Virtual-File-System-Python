from os import mkdir
import sqlite3
from sqlite3.dbapi2 import connect
from time import time_ns
import datetime
import os

def create_fs(name:str="filesystem", max_size:int=0):
  with sqlite3.connect(f"{name}.nvvfsd") as con:
    cur = con.cursor()

    cur.execute('''
    CREATE TABLE "directories" (
      "id"      INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
      "root_id" INTEGER NOT NULL,
      "type"    INTEGER,
      "name"    TEXT,
      "created" TEXT
    );
    ''')

    cur.execute('''
    CREATE TABLE "files" (
      "id"      INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
      "dir_id"  INTEGER NOT NULL,
      "name"    TEXT,
      "created" TEXT,
      "edited"  TEXT
    );
    ''')

    now = datetime.datetime.now()
    cur.execute('''
    INSERT INTO directories VALUES (0, 0, 1, "", :date);
    ''', {"date": f"{time_ns()}|{now.year}|{now.month}|{now.day}|{now.hour}|{now.minute}"})

    con.commit()

    mkdir("files")

class NVVFSDate:
  @staticmethod
  def decode(date:str=""):
    data = date.split("|")
    return {
      "time":   data[0],
      "year":   data[1],
      "month":  data[2],
      "day":    data[3],
      "hour":   data[4],
      "minute": data[5],
    }
  
  @staticmethod
  def encode(date:dict={}):
    return "|".join([
      date["time"],
      date["year"],
      date["month"],
      date["day"],
      date["hour"],
      date["minute"],
    ])

class VirtualFS:
  def __init__(self, name:str):
    self.FS_NAME = f"{name}.nvvfsd"
  
  def execute(self, sql:str, kwargs={}):
    with sqlite3.connect(self.FS_NAME) as con:
      cur = con.cursor()

      cur.execute(sql, kwargs)
      con.commit()

      return cur.fetchall()
  
  def get_now_time(self):
    now = datetime.datetime.now()
    return f"{time_ns()}|{now.year}|{now.month}|{now.day}|{now.hour}|{now.minute}"

  def get_id(self, name:str=""):
    try:
      return int(self.execute('''
      SELECT seq FROM sqlite_sequence WHERE name=:name; 
      ''', {"name": name})[0][0]) + 1
    except:
      return 0
  
  def create_dir(self, root:int=0, name:str=""):
    self.execute('''
    INSERT INTO directories VALUES (:id, :root, 0, :name, :date);
    ''', {"id": self.get_id("directories"), "root": root, "name": name, "date": self.get_now_time()})
  
  def get_dirs(self, root:int=0):
    return self.execute('''
    SELECT id FROM directories WHERE root_id=:root AND type != 1;
    ''', {"root": root})

  def get_dir_data(self, id:int=0):
    raw_data = self.execute('''
    SELECT name, created, root_id FROM directories WHERE id=:id
    ''', {"id": id})[0]
    return {
      "name":    raw_data[0],
      "created": raw_data[1],
      "root":    raw_data[2],
    }
  
  def create_file(self, root:int=0, name:str=""):
    id = self.get_id("files")
    self.execute('''
    INSERT INTO files VALUES (:id, :root, :name, :date, :date);
    ''', {"id": id, "root": root, "name": name, "date": self.get_now_time()})

    with open(f"files/{id}.nvvfsf", "w") as file:
      pass
  
  def get_files(self, root:int=0):
    return self.execute('''
    SELECT id FROM files WHERE dir_id=:root;
    ''', {"root": root})
  
  def get_file_data(self, id:int=0):
    raw_data = self.execute('''
    SELECT name, created, edited, dir_id FROM files WHERE id=:id
    ''', {"id": id})[0]
    return {
      "name":    raw_data[0],
      "created": raw_data[1],
      "edited":  raw_data[2],
      "root":    raw_data[3],
    }
  
  def delete_file(self, id:int=0):
    self.execute('''
    DELETE FROM files WHERE id=:id
    ''', {"id": id})
    os.remove(f"files/{id}.nvvfsf")
  
  def edit_file(self, id:int=0, content:str=0):
    with open(f"files/{id}.nvvfsf", "w") as file:
      file.write(content)
    
    self.execute('''
    UPDATE files SET edited=:date WHERE id=:id
    ''', {"date": self.get_now_time(), "id": id})
  
  def read_file(self, id:int=0):
    with open(f"files/{id}.nvvfsf", "r") as file:
      return file.read()

  def raw_delete_dir(self, id:int=0):
    self.execute('''
    DELETE FROM directories WHERE id=:id;
    ''', {"id":id})

  def delete_dir(self, id:int=0):
    if id == 0:
      return
    self.raw_delete_dir(id)
    self.execute('''DELETE FROM files WHERE dir_id=:root''', {"root": id})

    _delete = []

    while True:
      dirs = self.execute('''SELECT * FROM directories''')

      _delete = [dir[0] for dir in dirs if dir[0] not in [i[1] for i in dirs]]

      if _delete == []:
        break
      for id in _delete:
        self.execute('''DELETE FROM files WHERE dir_id=:root''', {"root": id})
        self.raw_delete_dir(id)
