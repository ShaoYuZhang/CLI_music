import os.path
import os
import hashlib

class Song:
  def __init__(self, path):
    self.raw_path = path
    self.hash_val = None

  def missing_hash(self):
    return self.hash_val is None

  def hash(self):
    if not self.hash_val: 
      self.hash_val = hashlib.sha1(open(self.abspath(), 'rb').read()).hexdigest()
    return self.hash_val

  def name(self):
    return os.path.basename(self.raw_path)

  def path(self):
    return '"{0}"'.format(self.raw_path)

  def abspath(self):
    return os.path.abspath(self.raw_path)

  def delete(self):
    os.remove(self.raw_path)
