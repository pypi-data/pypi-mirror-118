import json
import numbers
import sys, os

# Disable
def blockPrint(): sys.stdout = open(os.devnull, 'w')
# Restore
def enablePrint(): sys.stdout = sys.__stdout__

def test():
    print("Package is Linked & Working")

#Root Level
def doc(content, carryForward=None):
    print("Parsing Doc: " + json.dumps(content))
    text=""
    for c in content:
        text += parse(c)
        pass
    return text

#Top Level
def blockquote(content, carryForward=None):
    print("Parsing BlockQuote: " + json.dumps(content))
    text=""
    for c in content:
        text += parse(c)
    return text

def paragraph(content, carryForward=None):
    print("Parsing Paragraph: " + json.dumps(content))
    text=""
    for c in content:
        text += parse(c)
    return text+"\n"

def bulletList(content, carryForward=None):    
    print("Parsing Bulletlist: " + json.dumps(content))
    text="\n"
    #carryForward=1
    carryForward='*'
    for c in content:
        text += parse(c, carryForward)
        #carryForward += 1
    return text

def orderedList(content, carryForward=None):
    print("Parsing OrderedList: " + json.dumps(content))
    text="\n"
    carryForward=1
    for c in content:
        text += parse(c, carryForward)
        carryForward += 1
    return text

def codeBlock(content, carryForward=None):
    print("Parsing CodeBlock: " + json.dumps(content))
    text=""
    for c in content:
        text += parse(c)
    return text

def heading(content, carryForward=None):
    print("Parsing Heading: " + json.dumps(content))
    text=""
    for c in content:
        text += parse(c)
    return text+"\n"

#Child Level
def listItem(content, carryForward):
    print("Parsing ListItem: " + json.dumps(content))
    text=""
    for c in content:
        text += ((str(carryForward)+". ") if isinstance(carryForward, numbers.Number) else carryForward+" ")+parse(c)+'\n'
        #text += "* "+parse(c)+', '
    return text


#Inline Level
def text(obj, carryForward=None):
    print("Parsing Text: " + json.dumps(obj))
    text=obj['text']
    if obj.get('marks'):
        #Search for Marks
        for m in obj.get("marks"):
            try: text += parse(m)
            except: pass
    return text

def link(attrs, carryForward=None):
    print("Parsing Link")
    return "("+attrs.get("href")+")"

def mention(attrs, carryForward=None):
    print("Parsing Mention")
    return attrs.get("text")

def emoji(attrs, carryForward=None):
    print("Parsing Emoji")
    return attrs.get("text")

def hardBreak(data=None, carryForward=None):
    print("Parsing HardBreak")
    return '\n'


#Driver Functions
def parse(adf, carryForward=None, debug=False):
    if debug==False: blockPrint()
    switcher = {
        "doc": (doc, 'content'),
        "blockquote": (blockquote, 'content'),
        "paragraph": (paragraph, 'content'),
        "text": (text, 'self'),
        "hardBreak": (hardBreak, ''),
        "bulletList": (bulletList, 'content'),
        "orderedList": (orderedList, 'content'),
        "listItem": (listItem, 'content'),
        "codeBlock": (codeBlock, 'content'),
        "heading": (heading, 'content'),
        "link": (link, 'attrs'),
        "mention": (mention, 'attrs'),                          #Available only with type="text"
        "emoji": (emoji, 'attrs')
    }
    type=switcher.get(adf['type'])                              #Get the ADF Type | Ex: "paragraph"
    fn=type[0]                                                  #Get the Function | Ex: paragraph()
    data=adf if type[1]=="self" else adf.get(type[1], None)     #Get the data to parse | Ex: "content" or "attrs" or "text"
    try: 
        result=fn(data, carryForward)                           #Ex: listItem(adf["content"], 1)
        enablePrint()
        return result
    except: 
        enablePrint()
        return ''
