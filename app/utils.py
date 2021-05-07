from pathlib import Path
import hashlib

""" ---- Application Macros ----"""
WEIGHTS_DIRPATH = "app/model/weights"
PIPELINES_DIRPATH = "app/model/pipelines"
LOGS_DIRPATH = "app/model/logs"
IMAGE_CLASSIFICATION_CLASSMAP_FILENAME = "Class Map"

def getNumberOfClasses(map_filepath):
  class_map = getClassMappingFromFile(map_filepath)
  return len(class_map)

def getClassMappingFromFile(map_filepath):
  class_map = {}
  with open(map_filepath) as reader:
    line = reader.readline()
    while line != '':
      # No error handling, if it becomes a problem write a regex
      name, index = line.split(": ")
      class_map[name] = int(index)
      line = reader.readline()
  return class_map

def getClassMappingFromDirectory(map_dirpath):
  # No error handling, whoops
  class_map = {}
  for path in Path(map_dirpath).iterdir():
    if path.name == IMAGE_CLASSIFICATION_CLASSMAP_FILENAME + ".txt":
      class_map = getClassMappingFromFile(str(path))
  return class_map

def runNameUnique(run_name):
  # Check for unique run name inside weight directory
  for pipeline_path in Path(WEIGHTS_DIRPATH).iterdir():
    for weights in pipeline_path.iterdir():
      if weights.name == run_name:
        return False
  return True

# Hash Helper
def md5_update_from_dir(directory, hash):
    assert Path(directory).is_dir()
    for path in sorted(Path(directory).iterdir(), key=lambda p: str(p).lower()):
        hash.update(path.name.encode())
        if path.is_file():
            with open(path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash.update(chunk)
        elif path.is_dir():
            hash = md5_update_from_dir(path, hash)
    return hash

# Hash Directory function, source: https://stackoverflow.com/questions/24937495/how-can-i-calculate-a-hash-for-a-filesystem-directory-using-python
def md5_dir(directory):
    return md5_update_from_dir(directory, hashlib.md5()).hexdigest()

def getSignalValue(signal):
  return int(signal)

# Unit Testing
# if __name__ == '__main__':
#   print(runNameUnique("Experiment 90"))
#   print(getClassMappingFromFile("model/Class Map.txt"))
#   print(getNumberOfClasses("model/Class Map.txt"))
#   print(getClassMappingFromDirectory("model"))