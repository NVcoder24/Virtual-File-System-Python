# Virtual File System Python
NVVFS. My own Virtual File System based on sqlite3!  
The concept of this File System is that  
everything works through IDs  

## Import module
```python
import nvvfs
```

## create File System
```python
# create fs
# will create fs_name.nvvfsd
# and files directory!
nvvfs.create_fs("fs_name")
```

## open File System
```python
# will open your file system
my_fs = nvvfs.VirtualFS("fs_name")

# or
with nvvfs.VirtualFS("fs_name") as my_fs:
  # do your magic here
```

## directories
```python
# create directory (root directory id is always 0)
my_fs.create_dir(root=0, name="my dir")    # will get id 1
my_fs.create_dir(root=0, name="other dir") # will get id 2

# first argument is root directory id
my_fs.get_dirs(0) # output: [(1, ), (2, )] or smth

# "created" is NVVFSDate time format
my_fs.get_dir_data(1) # output: {"name": "my dir", "created": "TIME", "root": 0}

# will delete everything in dir (files, other directories)
# root directory cannot be deleted!
my_fs.delete_dir(1)
```

## files
```python
# create file (extention doesnt matter at all)
my_fs.create_file(root=0, name="my file.txt")

# get files in directory
my_fs.get_files(0) # output: [(0, )]

# get file data
my_fs.get_file_data(0) # will return dict

# edit file
my_fs.edit_file(0, "File content here!")

# read file
my_fs.read_file(0) # output: File content here!

# delete file
my_fs.delete_file(0)
```

## NVVFSDate time format
This is a special time format for this File System.

```python
# this class does not have __init__ method!
# do not try to init!
nvvfs.NVVFSDate
```

```python
# you can do this if you want
fs_time = nvvfs.NVVFSDate

# decode time
time = fs_time.decode("TIME") # will output dict

# encode time for File System
fs_time.encode(time) # will output string
```

## Extra
There is some hidden function  
that are used by main methods  
NEVER USE THESE METHODS!
```python
# execute() to directly execute
# queries in database
my_fs.execute('''DROP TABLE files''') # THIS CODE WILL CORRUPT YOUR FILE SYSTEM
# (will drop table with files IDs and meta)

# raw_delete_dir() to delete
# one directory
# used by delete_dir()
my_fs.raw_delete_dir(1)
# this method dont check
# directory type and
# can corrupt your File System

# get_id() is used to
# get unique ID for
# file or directory
my_fs.get_id()

# get_now_time() is used to
# get current time in
# NVVFSDate time format
my_fs.get_now_time()
```

## Summary
This is first version of NVVFS<br>
(NVcoder Virtual File System)<br>
It is
- Fast
- Reliable
- Free
- Optimized
- Secure

It can be used for projects  
like cloud storage system  
where you need speed and security

## Feauture updates
Many possibilities for customizing  
Aka. max size, file types  
And File System interface for debug
