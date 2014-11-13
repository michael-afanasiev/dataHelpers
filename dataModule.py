class colours:
      HEADER = '\033[95m'
      OKBLUE = '\033[94m'
      OKGREEN = '\033[92m'
      WARNING = '\033[93m'
      FAIL = '\033[91m'
      ENDC = '\033[0m'

def getStations (fName, format='justified'):
  
  '''
  Little function to return the station code and network codes.
  '''
  
  stations = []
  networks = []
  f = open (fName, 'r')
  for line in f:
    
    fields = line.split ()
    
    # Don't include duplicate stations.
    if fields[0].ljust(4) in stations:
      continue
 
    if (format == 'justified'):
      stations.append (fields[0].ljust(4))
      networks.append (fields[1].ljust(2))
    else:
      stations.append (fields[0])
      networks.append (fields[1])
    
  return stations, networks
  
