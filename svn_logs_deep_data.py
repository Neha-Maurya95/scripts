
import pandas as pd
import subprocess
import xml.etree.ElementTree as ET
import csv
import os
import re
#start_date = "2023-01-01 00:00:00"
#end_date = "2023-04-17 00:00:00"
start_date = input("Enter Start Date in format (YYYY-MM-DD) : ")
end_date = input("Enter in format (YYYY-MM-DD) : ")
username = input("Enter username: ")
password = input("Enter password: ")

# Read the Excel file
df = pd.read_excel('/home/neha/SVN.xlsx')

# Extract the repository links from the second column
repo_links = df.iloc[:, 1]

# Initialize the rows list outside the loop
rows = []

# Loop th	rough the repository links and get the log information
for link in repo_links:
    # Check if the link starts with 'http://' or 'https://'
    if not link.startswith('http://') and not link.startswith('https://'):
        link = 'http://' + link

    command = ['svn', 'log', '-v', '--xml', '-r', "{" + start_date + "}:{" + end_date + "}", '--username', username, '--password', password, link]
    try:
        output = subprocess.check_output(command)
    except subprocess.CalledProcessError:
        # Authentication error, continue to the next repository link
        print(f"Authentication error for {link}")
        continue

    # Parse the XML output and extract the required fields
    log_data = ET.fromstring(output)
    for log_entry in log_data.iter('logentry'):
        revision = log_entry.attrib['revision']
        author = log_entry.find('author').text
        date = log_entry.find('date').text
        message = log_entry.find('msg').text
        for path in log_entry.iter('path'):
            action = path.attrib['action']
            path_content = path.text
            #row = [link, revision, author, date, message, action, path_content]
            #rows.append(row)

            # Execute the SVN diff command and get the output
            command = ['svn', 'diff', '-r', str(int(revision)-1)+':'+revision, '--username', username, '--password', password, link + '/' + path_content]
            print(command)
            try:
                diff_output = subprocess.check_output(command)
            except subprocess.CalledProcessError:
                # Authentication error, continue to the next repository link
                print(f"Authentication error for {link}")
                continue
            if 'svn:mime-type' in diff_output.decode('iso-8859-1'):
                #num_lines_modified = 'binary file'
                insertion = "binary_file"
                deletion = "binary_file"

                #print(num_lines_modified)
            else:
                diff_output = subprocess.check_output(command)
                num_lines_modified = diff_output.decode('ISO 8859-1').count('\n')
                diffstat_command = ['diffstat', '-s']
                diffstat_output = subprocess.check_output(diffstat_command, input=diff_output)
                #num_lines_modified = int(diffstat_output.split()[3])
                num_lines_modified_count = re.findall(r'\d+', diffstat_output.decode('utf-8'))
                if len(num_lines_modified_count) == 1:
                    insertion = "0"
                    deletion = "0"
                elif len(num_lines_modified_count) == 2:
                    insertion = int(num_lines_modified_count[1])
                    deletion = "0"
                elif len(num_lines_modified_count) == 3:
                    insertion = int(num_lines_modified_count[1])
                    deletion = int(num_lines_modified_count[2])
                else:
                    insertion = ""
                    deletion = ""
                #print("file does not conatins mimetype")
            # Add the row to the list of rows
            row = [link, revision, author, date, message, action, path_content, insertion, deletion]
            rows.append(row)

# Write the extracted data to a CSV file
with open('svn_log.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['RepoURL', 'Revision', 'Author', 'Date', 'Commit Message', 'Path Content', 'Files Changed', 'Lines Added', 'Lines Deleted'])
    writer.writerows(rows)

print("SVN log data extracted and saved to svn_log.csv")
