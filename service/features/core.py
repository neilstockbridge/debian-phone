
def contents_of( path_to_file):
  f = open( path_to_file)
  contents = f.read()
  f.close()
  return contents


def write_to_file( data, path_to_file):
  f = open( path_to_file, "w")
  f.write( data)
  f.close()

