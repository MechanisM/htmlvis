import os
import re
import urllib
from xml.etree import ElementTree


class VisToHtml:

    def __init__(self, output_filename, template):
        self.template = template
        self.output_filename = output_filename
        fin = open('templates/raw/' + self.template, 'r')
        self.original_template = fin.read()
        self.rendered_template = self.original_template
        self.replace_tags()
        self.save_rendered()
        self.generate_image()
        
    def replace_tags(self):
        xml_pattern = re.compile('({{\s*(\w+)\|([\w:/\.]+)\|(\w+)\s*}})')
        for xml_item in re.findall(xml_pattern, self.original_template):
            original, itemtype, url, xpath = xml_item
            self.replace_xml(original, url, xpath)
            
    def replace_xml(self, original, url, xpath):
        try:
          tree = ElementTree.parse(urllib.urlopen(url))
          text = tree.find('//' + xpath).text
          self.rendered_template = self.rendered_template.replace(original, text)
        except Exception, e:
          pass

    def save_rendered(self):
        fout = open('templates/rendered/' + self.template, 'w')
        fout.write(self.rendered_template)
        fout.close()
        
    def generate_image(self):
        base = '/Users/sam/Desktop/htmlvis'
        url = 'file://' + base + '/templates/rendered/' + self.template
        command = 'python2.6 webkit2png.py -D %s/output --filename %s --delay 1 %s' % (base, self.output_filename, url, )
        os.system(command)

v = VisToHtml('nowplaying', 'test.html')