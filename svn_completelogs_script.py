import pandas as pd
import subprocess
import xml.etree.ElementTree as ET
import csv

#start_date = "2018-01-01 00:00:00"
#end_date = "2023-04-17 00:00:00"
start_date = input("Enter Start Date in format (YYYY-MM-DD) : ")
end_date = input("Enter in format (YYYY-MM-DD) : ")
username = input("Enter username: ")
password = input("Enter password: ")

#username = 'gitesh.satywali'
#password = 'Netsmartz@123*'


# Read the Excel file
df = pd.read_excel('/home/neha/Downloads/SVN.xlsx')

# Extract the repository links from the second column
repo_links = df.iloc[:, 1]

# Initialize the rows list outside the loop
rows = []

# Loop th	rough the repository links and get the log information
for link in repo_links:
    # Check if the link starts with 'http://' or 'https://'
    if not link.startswith('http://') and not link.startswith('https://'):
        link = 'http://' + link

    # Command to execute the SVN log and get the XML output
    #command = ['svn', 'log', '-v', '--xml', '-r', "{" + start_date + "}:{" + end_date + "}", '--username', username, '--password', password, link]
    #output = subprocess.check_output(command)

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
            row = [link, revision, author, date, message, action, path_content]
            rows.append(row)

# Write the extracted data to a CSV file
with open('svn_log.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['RepoURL', 'Revision', 'Author', 'Date', 'Commit Message', 'Action', 'Path Content'])
    writer.writerows(rows)

print("SVN log data extracted and saved to svn_log.csv")
