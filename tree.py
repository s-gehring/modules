import network
import string
import io
import pdf_files as pdf

global_leaves= 0
global_nodes = 0
global_lectures=0


def get_tree(link, deep_search=False, first_iteration=True):
    global global_leaves, global_nodes
    c = network.get_content(link)
    #print c.prettify()
    if is_leaf(c):
        #leaf
        global_leaves = global_leaves + 1
        tables = c.find("div", class_="content").hr.find_all("table", recursive=False)
        if(deep_search):
          final_links = get_leaves(tables)
          return parsed_lectures_deeply(final_links)
        else:
          return parsed_lectures_shallow(tables)

    else:
        #node
        global_nodes = global_nodes + 1
        if c.div.hr == None:
          tables = c.find("div", class_="content").hr.find_all("table", recursive=False)
        else:
          tables = c.div.hr.find_all("table", recursive=False)
        new_title, new_links = get_nodes(tables)
        arr = {}
        i = 1

        for l in new_links:
            if first_iteration:
              print round(i*100./len(new_links),2),"% ("+l+")"
              i=i+1
            arr.update({l:get_tree(get_hyper_reference(new_links[l]), deep_search, False)})
        return arr

def get_link_padding(link_container):
    return int(link_container.tr.td['width'])

def get_link_title(link_container):
    # The string is hidden in about 32529 containers. Sorry
    # for not having a more descriptive comment,
    # but I don't have any idea how this works, I just found this to
    # be working.
    return link_container.tr.find_all("td")[1].table.tr.find_all("td")[2].a.string

def get_hyper_reference(link_container):
    return link_container.tr.find_all("td")[1].table.tr.find_all("td")[2].a['href']

def has_link_title(link_container):
    # Derived from get_link_title. There are empty tables
    # in between the full ones, so we check for these and ignore them.
    return link_container.tr.find_all("td")[1].table != None


def is_leaf(content):
  s = content.get_text().lower()
  buzzwords1 = ["day", "time", "room", "lecturer", "remarks", "duration"]
  buzzwords2 = ["tag", "zeit", "raum", "lehrperson", "bemerkung", "dauer"]
  buzzwords3 = [u"(--- lecture not found ---)", u"(--- keine veranstaltung in diesem bereich gefunden ---)"]
  failed = False
  for x in buzzwords3:
    if x in s:
      return True
  for x in buzzwords1:
    if x not in s:
      failed = True
      break
  if not failed:
    return True
  for x in buzzwords2:
    if x not in s:
      return False
  return True



def parsed_lectures_shallow(tables):
  global global_lectures
  parsed_data = []
  for table in tables:
    if table.tr.td.has_attr("width"):
      # Not real. Find last title though.
      pass
    else:

      data_containers = table.find_all("tr")[1].find_all("td")[1].find_all("table")
      # Now we need data_containers (which are <table>s) in packs of two.
      # We use this boolean to handle this
      first = True
      cur_lecture = {}
      for container in data_containers:

        if first:
          actual_container = list(container.tr.td.children)

          full_title = actual_container[1].a.string
          title_parts = string.split(full_title, u' - ')
          if len(title_parts) < 2:
            small_id = None
            full_title = title_parts[0]
          else:
            small_id = io.clean_string(title_parts[0])
            full_title = io.clean_string(title_parts[1])

          actual_container = list(actual_container[3].children)

          no_and_time = actual_container[0].string
          no_and_time = no_and_time.split(u"\xa0")
          number = io.clean_string(no_and_time[0])
          time = io.clean_string(no_and_time[3])

          lec_type = io.clean_string(actual_container[1].string)

          if isinstance(actual_container[2], basestring):
            effort = io.clean_string(actual_container[2])
            if actual_container[3].a == None or actual_container[3].a.string == None:
              lecturer = None
            else:
              lecturer = io.clean_string(actual_container[3].a.string)
          else:
            effort = None
            if actual_container[2].a == None or actual_container[2].a.string == None:
              lecturer = None
            else:
              lecturer = io.clean_string(actual_container[2].a.string)

          if small_id == None:
            pdf_pages = []
          else:
            pdf_pages = pdf.get_pdf_pages(small_id)

          cur_lecture = {
              "title":full_title,
              "id":number,
              "type":lec_type,
              "time":time,
              "effort":effort,
              "small_id":small_id,
              "lecturer":lecturer,
              "pages":pdf_pages
          }

        else:
          # Time table... *sigh*
          global_lectures = global_lectures +1
          times = []

          for tr in container.find_all("tr"):
            if tr.td == None:
              continue
            if tr.th != None:
              continue

            # now we don't have the first two, and not the last k tds.
            # we can actually start building our timetable
            tds = list(tr.find_all("td"))
            if len(tds) < 7:
              continue
            weekday = io.get_weekday(io.clean_string(tds[1].string))

            if tds[2].nobr.string == None:
              time = None
            else:
              time = tds[2].nobr.string.strip()
            if tds[3].a.string == None:
              room = None
            else:
              room = {'name':tds[3].a.string, 'link':tds[3].a['href']}
            if tds[4].string == None:
              lecturer = None
            else:
              lecturer = tds[4].string.strip()
            if tds[5].string == None:
              notes = None
            else:
              notes = tds[5].string.strip()
            if tds[6].string == None:
              duration = None
            else:
              duration = io.clean_string(tds[6].string.replace("<br>", "").replace("bis", "to"))

            times.append({
              'day':weekday,
              'time':time,
              'room':room,
              'lecturer':lecturer,
              'notes':notes,
              'duration':duration
            })
            cur_lecture.update({'schedule':times})
          parsed_data.append(cur_lecture)
          pass

        first = not first

  return parsed_data


def parse_links(container):
    first = True
    resulting_links = []
    for table in container:
        if first:
            resulting_links.append(table.tr.td.h2.a['href'])

        first = not first
    return resulting_links

def get_leaves(links):
    right_amount_of_links = []

    for link in links:
        # Now we don't have any empty tables anymore.
        if not link.tr.td.has_attr('width'):

            # Now we have our real tables
            # with actual data in it.
            # We ignore this data aswell
            # and look for the link for the
            # dedicated page.
            right_amount_of_links.extend(parse_links(link.find_all("tr")[1].find_all("td")[1].find_all("table")))

            # Or maybe we don't?


    return right_amount_of_links

def get_nodes(links):
    max_padding = -1
    cur_title = "This should not be visible ever #1"
    last_title= "This should not be visible ever #2"
    right_amount_of_links = {}
    for link in links:
        if not has_link_title(link):
            continue
        cur_padding = get_link_padding(link)
        if(max_padding < cur_padding):

            last_title = cur_title
            max_padding = cur_padding
            cur_title = get_link_title(link)
            right_amount_of_links = {cur_title:link}
        else:
            cur_title = get_link_title(link)
            right_amount_of_links.update({cur_title:link})

    return last_title, right_amount_of_links

def parse_lecture_deeply(link):
    c = get_content(link)
    d = c.find("div", class_="content").form

    e = d.find_all("table", recursive=False)
    # In e[0]: MA-INF 0402 - Master Thesis Seminar - Single View

    full_title = e[0].tr.td.h1.string

    title_parts = string.split(full_title, u' - ')
    small_id = io.clean_string(title_parts[0])
    full_title = io.clean_string(title_parts[1].strip())


    # In f: Nr.: 612010402     Seminar    WiSe 2016/17     2.0 Hours per week in term
    f = list(e[1].tr.td.children)
    index = 2

    if len(f) < 4:
        index = 0
        number = None
    else:
        number = f[1].string

    lec_type = io.clean_string(f[1+index].string)

    time_and_effort = f[2+index]
    tae = string.split(time_and_effort, u'\xa0')
    time = io.clean_string(tae[0])
    effort = io.clean_string(tae[3])

    #e[2] is just "That's a masters  course
    index = 3
    if(e[index].tr == None):
        index = 2
    lecturer = e[index].tr.find_all("td")
    if(len(lecturer) > 1):
        lecturer = io.clean_string(lecturer[1].a.string)
    else:
        lecturer = None

    return {
        "title":full_title,
        "id":number,
        "type":lec_type,
        "time":time,
        "effort":effort,
        "small_id":small_id,
        "lecturer":lecturer
    }


def parsed_lectures_deeply(links):
    parsed_data = []
    global global_lectures
    for link in links:
        global_lectures = global_lectures +1
        d = parse_lecture_deeply(link)
        d.update({'link':link})
        parsed_data.append(d)
    return parsed_data
