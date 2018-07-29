import HTMLParser
from htmlentitydefs import name2codepoint

class _MyHTMLParser(HTMLParser.HTMLParser):
    def __init__(self,classinit):
        HTMLParser.HTMLParser.__init__(self)
        self.root = None
        self.stack = []
        self.classinit = classinit
    def handle_starttag(self, tag, attrs):
        closed = tag not in ['img','br']
        node = self.classinit(tag,{k: v for k, v in attrs},[],closed)
        if not self.root:
            self.root = node
        if self.stack:
            self.stack[-1].content.append(node)
        if closed:
            self.stack.append(node)
    def handle_endtag(self, tag):
        if self.stack and self.stack[-1].tag == tag:
            self.stack[-1].opentag = False
            self.stack = self.stack[:-1]
    def handle_data(self, data):
        if not self.stack: return
        self.stack[-1].content.append(self.classinit('_text_',{},data))
    def handle_comment(self, data):
        pass
    def handle_entityref(self, name):
        if name in name2codepoint:
            c = unichr(name2codepoint[name])
        else:
            c = '&'+name
        if not self.stack: return
        self.stack[-1].content.append(self.classinit('_text_',{},c))
    def handle_charref(self, name):
        if name.startswith('x'):
            c = unichr(int(name[1:], 16))
        else:
            c = unichr(int(name))
        if not self.stack: return
        self.stack[-1].content.append(self.classinit('_text_',{},c))
    def handle_decl(self, data):
        pass

def parse(text,classinit):
    parser = _MyHTMLParser(classinit)
    parser.feed(text)
    return parser.root
    
