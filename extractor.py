import sys, httplib2, urllib
from html.parser import HTMLParser

class GalleryParser(HTMLParser):
    def __init__(self, name):
        self.file = open(name, 'w')
        HTMLParser.__init__(self)
        self.start_tag_found = False
        self.inside_image_div = 0
        self.link_retrieved = False
        self.tag_case = 0
        # 0 implies a tag was never found,
        # 1 = imgur.com/gallery/{hash}
        # 2 = imgur.com/a/{hash}
        # 3 = imgur.com/a/{hash}/all

    def handle_starttag(self, tag, attrs):
        if self.start_tag_found:
            if self.tag_case == 1:
               if self.inside_image_div > 0:
                   if tag == 'img':
                        for name, value in attrs:
                            if name == 'src':
                                    print(clean_url(value))
                                    self.file.write(clean_url(value) + '\n')

               elif tag == 'div':
                   for name, value in attrs:
                       if name == 'class' and value == 'album-image':
                           self.inside_image_div = 2 # There are Two Divs that need to be escaped
            elif self.tag_case == 2:
               if self.inside_image_div > 0:
                   if tag == 'a':
                        for name, value in attrs:
                            if name == 'href':
                                if not self.link_retrieved:
                                    self.link_retrieved = True
                                    print(clean_url(value))
                                    self.file.write(clean_url(value) + '\n')
               elif tag == 'div':
                   for name, value in attrs:
                       if name == 'class' and value == 'image':
                           self.link_retrieved = False
                           self.inside_image_div = 7 # There are Seven Divs that need to be escaped

            elif self.tag_case == 3:
               if self.inside_image_div > 0:
                   if tag == 'img':
                        for name, value in attrs:
                            if name == 'src':
                                if not self.link_retrieved:
                                    self.link_retrieved = True
                                    print(clean_url(value))
                                    self.file.write(clean_url(value) + '\n')
               elif tag == 'div':
                   for name, value in attrs:
                       if name == 'class' and value == 'post':
                           self.link_retrieved = False
                           self.inside_image_div = 1 # There are Seven Divs that need to be escaped
        else:
            if tag == 'div':
                for name, value in attrs:
                    if name == 'id' and value == 'image':
                        self.start_tag_found = True
                        self.tag_case = 1; # url format = imgur.com/gallery/xxxxx
                    elif name == 'id' and value == 'image-container':
                        self.start_tag_found = True
                        self.tag_case = 2; # url format = imgur.com/a/xxxxx
                    elif name == 'class' and value == 'posts':
                        self.start_tag_found = True
                        self.tag_case = 3; # url format = imgur.com/a/xxxxx/all

    def handle_endtag(self, tag):
        if tag == 'div':
            # if div tag is found and we are inside an image div tag, don't close parser yet
            if self.inside_image_div > 0:
                self.inside_image_div -= 1
            elif self.start_tag_found:
                self.file.close()
                self.close(self)

def clean_url(Url):
    return Url[2:]

# Check for proper arguments and syntax
if len(sys.argv) < 2:
    print("Usage: extract.py [URL] [OUTPUT_FILE]")
    sys.exit(2)

http = httplib2.Http()
resp, content = http.request(sys.argv[1], "GET")

file_name = sys.argv[2]
parser = GalleryParser(file_name)
str_content = content.decode('utf-8')

try:
    print("Starting")
    parser.feed(str_content)
except (RuntimeError, TypeError, NameError):
    print("Stopping")