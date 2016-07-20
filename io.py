
def clean_string(s):
    return s.replace(u"\x0a", " ").strip()


def get_weekday(wd):
  wd = wd.lower()
  if wd == "mo" or wd == "fr" or wd == "sa":
    return wd
  if wd == "di":
    return "tu"
  if wd == "mi":
    return "we"
  if wd == "do":
    return "th"
  if wd == "so":
    return "su"
  return wd

#%%

def seconds_to_time(sec):
    days = int(sec / (24*3600))
    rem = sec - (days*24*3600)

    hours = int(rem / 3600)
    rem = rem - (hours*3600)

    minutes=int(rem / 60)
    rem = rem - (minutes*60)

    seconds=int(rem)
    rem = rem - seconds

    ms = int(rem*1000)

    if days > 0:
      return str(days)+":"+str(hours)+":"+str(minutes)+":"+str(seconds)+"."+str(ms)
    if hours> 0:
      return str(hours)+":"+str(minutes)+":"+str(seconds)+"."+str(ms)
    if minutes > 0:
      return str(minutes)+":"+str(seconds)+"."+str(ms)
    if seconds> 0:
      return str(seconds)+"."+str(ms)+"sec"
    return str(ms)+"ms"

