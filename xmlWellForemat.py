import xml.dom.minidom
import os


try:
    dir_path = "./wellFormatedXML"
    os.mkdir(dir_path)
    dir_path = "./wellFormatedXML/cars"
    os.mkdir(dir_path)
    dir_path = "./wellFormatedXML/cars/2007/"
    os.mkdir(dir_path)
    dir_path = "./wellFormatedXML/cars/2008/"
    os.mkdir(dir_path)
    dir_path = "./wellFormatedXML/cars/2009/"
    os.mkdir(dir_path)
except:
    None

root_directory = "./OpinRank"
fileList=[]
# Loop through all directories and subdirectories
for dirpath, dirnames, filenames in os.walk(root_directory):
    # Loop through all files in the current directory
    for filename in filenames:
        # Do something with the file
        file_path = os.path.join(dirpath, filename)
        fileList.append(file_path)

        # print(filenames)
# print(fileList)
for f in fileList:
    with open(f, 'r') as file:
        # print(f)
        # print(file_path)
        try:
            data = file.read().replace("&"," ")

            data = f'<ROOT>{data}</ROOT>'
            dom = xml.dom.minidom.parseString(data)
            pretty_xml = dom.toprettyxml()


        # Create a new directory
        # print(222)

        # Create a new file in the directory

            filename_new = f[11:]
            dir_path = "./wellFormatedXML"
            # print(filename_new)
            file_path_new = os.path.join(dir_path, filename_new)
            print(file_path_new)

            # Write the pretty XML to a file
            with open(file_path_new, 'w') as file:
                file.write(pretty_xml)

        except:
            None
        