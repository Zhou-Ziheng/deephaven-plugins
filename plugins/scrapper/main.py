import os
import requests
from bs4 import BeautifulSoup

def getFileNames(path):
    file_names = []
    
    # Check if the path exists
    if os.path.exists(path):
        # Get the list of files in the directory
        files = os.listdir(path)
        
        # Filter out only the files (excluding directories)
        file_names = [file for file in files if os.path.isfile(os.path.join(path, file))]

        for i in range(len(file_names)):
            file_names[i] = os.path.splitext(file_names[i])[0]
    return file_names

path = "./components"
fileNames = getFileNames(path)

class TypeLiteral():
    def __init__(self, literal):
        self.literal = literal

    def __str__(self):
        return self.literal

class Function():
    def __init__(self, typestring):
        print(typestring)
        self.typestring = typestring
        self.parameters = []


    def __str__(self):
        return '"' + "function hehe" + '"'
    
class Literal():
    def __init__(self, literal):
        self.literal = literal

    def __str__(self):
        return '"' + self.literal + '"'

class Type():
    def __init__(self, typestring):
        self.typestring = typestring
        self.types = []
        self.parseType()

    def parseType(self):
        if "(" in self.typestring:
            # typestring has a function somewhere, need to one at a time.
            string = self.typestring
            
            index = string.find("|")
            while index != -1:
                substring = string[:index]
                if "(" in substring:
                    # found a function, treat all "|" has paramter/return of function
                    self.types.append(Function(substring))
                else:
                    self.types.append(Type(substring))
                string = string[index+1:]
                index = string.find("|")
                
            if "(" in string:
                self.types.append(Function(string))
            else:
                self.types.append(Type(string))



            self.types.append(Function(self.typestring))
        elif "|" in self.typestring:
            splitted = self.typestring.split("|")
            for item in splitted:
                self.types.append(Type(item))
        elif self.typestring == "boolean":
            self.types.append(TypeLiteral("boolean"))
        elif self.typestring == "string":
            self.types.append(TypeLiteral("string"))
        else:
            clean = self.typestring.replace('\n', '').replace('\xa0', '').strip()
            if clean[0] == "'":
                self.types.append(Literal(clean.replace("'", '')))
            else:
                self.types.append(TypeLiteral(clean))

    def __str__(self):
        return "|".join([str(item) for item in self.types])
        
        

class Prop():
    # type:
    # 0: boolean
    # 1: string
    # 2: literal []
    # 3: literal
    def __init__(self, name, type, description):
        self.name = name
        self.type = Type(type)
        self.description = description

    def __str__(self):
        return self.name + ": " + str(self.type)
    
def parseRow(row):
    cols = row.find_all("td")
    # Name of the prop
    name = cols[0].text

    # Type
    type = cols[1].text

    # Description
    desc = cols[3].text

    return Prop(name, type, desc)



def parseTable(table):
    rows = table.find_all("tbody")[0].find_all("tr")
    props = []
    for row in rows:
        prop = parseRow(row)
        props.append(prop)

    return props
    

def getTypes(component):
    url = "https://react-spectrum.adobe.com/react-spectrum/" + component + ".html"

    # Make a GET request to fetch the raw HTML content
    response = requests.get(url)
    if response.status_code == 200:
        # Parse the html content
        soup = BeautifulSoup(response.content, "html.parser")

        # Get the list of types
        props = soup.find_all("table", class_=lambda value: value and 'propTable' in value)
        
        parsed = parseTable(props[0])

        

        # Filter out only the types
        # print(types)

        return parsed
    

for fileName in fileNames:
    props = getTypes(fileName)
    for prop in props:
        print(prop)
    
    print("======================================================")