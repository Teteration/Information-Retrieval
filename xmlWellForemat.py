import xml.dom.minidom

# Read in the file
with open('./OpinRank/cars/2008/2008_volkswagen_touareg_2', 'r') as file:
    # data = file.read()
    data = file.read().replace("&"," ")

# Add root tag to the data
data = f'<ROOT>{data}</ROOT>'

# Parse the data
dom = xml.dom.minidom.parseString(data)

# Pretty print the parsed XML data
pretty_xml = dom.toprettyxml()

# Remove root tag from the data
# pretty_xml = pretty_xml.replace('<ROOT>\n', '', 1).replace('</ROOT>', '', 1)

# Write the pretty XML to a file
with open('output2.xml', 'w') as file:
    file.write(pretty_xml)
