import os

class File:
  path: str
  name: str
  content: str

  def __init__(self, path, name):
    self.path = path
    self.name = name
    
  @property
  def full_path(self):
    return "%s/%s" % (self.path, self.name)
    
  @property
  def content(self):
    with open(self.full_path, 'r') as content:
      return [line.replace('\n', '') for line in content.readlines()]

class LineParser:
  types = ['import', 'message', 'service', 'rpc']
  content_type: str = None

  def __init__(self, line):
    for _type in self.types:
      if line.startswith(_type):
        self.content_type = _type
    
class ProtoFile(File):
  def parse_to_interface(self):
    for line in self.content:
      line_instance = LineParser(line)
      print(line_instance.content_type)

class Proto2Ts:
  INPUT_FOLDER = 'input'
  OUTPUT_FOLDER = 'output'

  files: list[File] = []
  
  def __init__(self):
    self.read_files()

    for file in self.files:
      file.parse_to_interface()

      for l in file.content:
        # print(l)
        pass


  def read_files(self):
    current_folder_index = 0
    folders = [self.INPUT_FOLDER]

    while len(folders) > current_folder_index:
      current_folder = folders[current_folder_index]
      _, subfolders, filenames = next(os.walk(current_folder), (None, None, []))
      
      if subfolders and len(subfolders) > 0:
        folders.extend([f"{current_folder}/{subfolder}" for subfolder in subfolders])
      
      self.files.extend([ProtoFile(current_folder, filename) for filename in filenames])
            
      current_folder_index += 1

instance = Proto2Ts()