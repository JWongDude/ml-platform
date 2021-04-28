from pathlib import Path

def numberOfClasses(directory):
  return len(list(Path(directory).iterdir()))