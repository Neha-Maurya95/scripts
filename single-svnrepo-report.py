import subprocess
import xml.etree.ElementTree as ET
import csv

svn_url = 'http://192.168.10.15/svn/alwaysbestcareV2'
start_date = "2018-01-01 00:00:00"
end_date = "2023-04-17 00:00:00"

username = 'gitesh.satywali'
password = 'Netsmartz@123*'


# Command to retrieve SVN logs in XML format
command = [
    "svn", "log", "-v", "--xml", "-r", "{" + start_date + "}:{"
    + end_date + "}", "--username", username, "--password", password, svn_url
]


# Command to execute the SVN log and get the XML output
command = ['svn', 'log', '-v', '--xml', '-r', "{" + start_date + "}:{" + end_date + "}", '--username', username, '--password', password, svn_url]
output = subprocess.check_output(command)

# Parse the XML output and extract the required fields
log_data = ET.fromstring(output)
rows = []
for log_entry in log_data.iter('logentry'):
    revision = log_entry.attrib['revision']
    author = log_entry.find('author').text
    date = log_entry.find('date').text
    message = log_entry.find('msg').text
    for path in log_entry.iter('path'):
        action = path.attrib['action']
        path_content = path.text
        row = [revision, author, date, message, action, path_content]
        rows.append(row)

# Write the extracted data to a CSV file
with open('svn_log.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Revision', 'Author', 'Date', 'Commit Message', 'Action', 'Path Content'])
    writer.writerows(rows)

print("SVN log data extracted and saved to svn_log.csv")
