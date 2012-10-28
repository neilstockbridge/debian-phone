
def usage():
  f = open("/proc/meminfo")
  value_on = lambda line: int( line.split()[1] )
  for line in f:
    if line.startswith("MemTotal:"):
      total = value_on( line)
    elif line.startswith("MemFree:"):
      free = value_on( line)
    elif line.startswith("Buffers:"):
      buffers = value_on( line)
    elif line.startswith("Cached:"):
      cached = value_on( line)
    elif line.startswith("SwapTotal:"):
      swap_total = value_on( line)
    elif line.startswith("SwapFree:"):
      swap_free = value_on( line)
      # SwapFree is the last line we're interested in so don't bother reading the rest:
      break
  f.close()
  return total, free, buffers, cached, swap_total, swap_free

