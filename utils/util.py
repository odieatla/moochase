import csv
import time
import os
from subprocess import call
from ftplib import FTP
from django.conf import settings

try:
  from lxml import etree
  print("running with lxml.etree")
except ImportError:
  try:
    # Python 2.5
    import xml.etree.cElementTree as etree
    print("running with cElementTree on Python 2.5+")
  except ImportError:
    try:
      # Python 2.5
      import xml.etree.ElementTree as etree
      print("running with ElementTree on Python 2.5+")
    except ImportError:
      try:
        # normal cElementTree install
        import cElementTree as etree
        print("running with cElementTree")
      except ImportError:
        try:
          # normal ElementTree install
          import elementtree.ElementTree as etree
          print("running with ElementTree")
        except ImportError:
          print("Failed to import ElementTree from any known place")
#ftp connection
def ftp_connection(server, user, password):
    return FTP(server, user, password)

#retrieve file from ftp. params: folder--location of .xml.gz file on ftp server; gz--name of .xml.gz file; vendor--vendor of data feed, default 'tms'
def retrieve_from_ftp(gz, folder=None, target_folder=settings.FILE_DIR, vendor='tms'):
    try: 
        ftp = ftp_connection(settings.FTP_SERVER[vendor], settings.FTP_USER[vendor], settings.FTP_PASSWORD[vendor])

        try:
            if folder is not None:
                ftp.cwd(folder)
        except:
            print("folder not none")
        try:
            target = os.path.join(target_folder, gz)
            ftp.retrbinary("RETR {0}".format(gz), open(target, 'wb').write)
        except:
            print("retrieve error")
        return target
    except:
        print("ftp download failed")

#since ftp file names from vendors are changing everyday, so we need to get the file name dynamically.
def get_ftp_file_name(pattern, file_date=time.strftime("%Y%m%d")):
    #for sample data:
    file_date = "20140516"

    return pattern.replace("YYYYMMDD", file_date)

def get_file_path(pattern, path=settings.FILE_DIR):
    #for sample data:
    file_date = "20140516"

    return os.path.join(path, pattern.replace("YYYYMMDD", file_date))

#decompress .gz file
def decompress_gz(gz):
    call("gzip -d {0}".format(gz).split(' '))

#load xml file to memory and return it
#params: xml--load from. path--path for collection
def load_xml_tree(xml, path):
    tree = etree.parse(xml)
    try:
        return tree.find(path)
    except:
        print "failed to load xml file %s" % xml

def load_to_csv(destination, data):
    csvfile  = open(destination, "wb")
    csv_writer = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL, delimiter='\t')
    for row in data:
        row = [c.encode('utf8') if isinstance(c, unicode) else c for c in row]
        csv_writer.writerow(row)

    csvfile.close()
    print "wrote %s" % destination
