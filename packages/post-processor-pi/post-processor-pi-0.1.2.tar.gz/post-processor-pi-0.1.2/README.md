**post-processor-pi** is a Python module that exploits the output of Document AI (tool available 
on GCP) to create a JSON file that stores the text contained in a document in an organized way, so 
that it reflects its original structure. To work with different types of 
documents having different structures, post-processor-pi has to be configured using the GUI
that I developed.

Installation
------------

The easiest way to install post-processor-pi is using pip:

    pip install post-processor-pi

Documentation
------------

As I mentioned above in order to implement the post-processor we need to configure it first and this
can be done using the Configuration GUI that I developed. 

### Configuration GUI 

In order to start the Configuration GUI we need an example corresponding to the output of Document
AI for one document. Below you can find the code example that enables you to start the Configuration
GUI.

```python
from dai_post_processor import post_processor as pp

# Open one example from Document AI output
path = "your/path/to/DocumentAI/example"
doc_ai = pp.open_doc_ai(path)

# Start Configuration GUI
mywin = pp.configGUI(doc_ai)
mywin.start()
```

After running the above instructions the GUI should open.

#### Configuration GUI Tuning

The Configuration GUI consists of two windows:

1) **Main**: here you can find the essential instructions that are needed to
 configure post-processor-pi.
    - **Select text of interest**: in this section you can select the portion
    of the pages in the documents you're interested in. In the **Page number** 
    field you can provide the page number of the Document example you want to open.
    I you press the **Draw Box** button a new window will open, and here you can
    select the portion of the page drawing a rectangle. All the text outside this
    rectangle will be ignored for all pages and documents. Once you performed the
    selection you can close the interactive window. Below you have a demo.
    <p align="center"><img src="https://github.com/paoloitaliani/post-processor-pi/raw/master/images/gui.gif" width=600></p>

    - Structuring Filter: in this section you can specify the first and second
    level *points* that give structure to the document. In the 
    **Main Structure** field you need to 
    specify the regex rule that lets you find all the first level *points*. If
    you press the **Add Point** button an additional field, where you can specify
    the regex rule for the second level *points*, will appear.
    
    - Output: in this section you can specify what to include in the JSON output
    of the Post Processor. You can choose to include the list of all lines and
    paragraphs in the document and the structured text. You can also choose to 
    ignore those lines that are recognised as *Headers* with the Filter Headers
    checkbox.
 
2) **Advanced**: here you can perform some more advanced configurations:

   - **Line threshold**: helpful for reconstructing lines in the document when 
   Document AI fails to do so. If the difference between the y top coordinates 
   of a line and the previous one is less than **Line Threshold** in absolute
   value, these two lines are merged together to form a new *reconstructed line*.
   
   - **Line repeat**: specify how many lines from the Document AI output are 
   needed to build a single *reconstructed line*
   
   - **Paragraph Multiplier**: helpful for reconstructing paragraphs in the 
   document when  Document AI fails to do so.
   Every line in the document that has a vertical
   gap with respect to the previous line lower than the median vertical gap of
   all lines in the document multiplied by the **Paragraph Multiplier**, will be
   appended to the previous line to form a paragraph.
   
   - **Header Multiplier**: has a similar role of the Paragraph Multiplier, but 
   it's useful for finding the centered headers in the document.
   
Once you're happy with your changes you can press the **Save** button and a 
configuration file will be created and saved as data/config.json


Example
------------

In this example I'm going to show how to implement post-processor-pi on the 
output of Document AI. The example document is a World Bank Loan Agreement and has
this kind of structure. 

<p align="center"><img src="https://github.com/paoloitaliani/post-processor-pi/raw/master/images/image1.png" width=600></p>

The first level points are the dotted numbers such as **2.07** and the second 
level points are the letters between round brackets such as **(a)**. Below you
can find the code implementation that lets create the structured JSON using the
config.json file that we created using the GUI.

```python
from dai_post_processor import post_processor as pp
import json

# Open one example from Document AI output
path = "your/path/to/DocumentAI/example"
doc_ai = pp.open_doc_ai(path)

# Open config.json file
with open("data/config.json") as json_file:
    config_dict = json.load(json_file)

# Apply the Post Processor to the Document AI output
doc_class = pp.DocumentClass(doc_ai, config_dict)
structured_doc = doc_class.create_json(file_name="example")
```
After running the above code the structured JSON will be saved as
data/pp_output/example.json. Below you can find a snippet of example.json, in 
particular the *structured_output* section. As you can see the JSON file reflects
the original structure of the document.

<p align="center"><img src="https://github.com/paoloitaliani/post-processor-pi/raw/master/images/image2.png" width=600></p>
