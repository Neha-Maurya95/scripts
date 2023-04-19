#!/bin/sh

sudo apt install xmlstarlet xlsx2csv -y
# set start and end dates 

echo "Enter the Start date in format YYYY-MM-DD: "
read start_date
echo "Enter the End date in format YYYY-MM-DD: "
read end_date

# set username and password for authentication
echo "Enter the username to checkout to svn repo: "
read svn_username
echo "Enter the password: "
read svn_password


# set path to CSV file containing repository URLs
repo_links=($(xlsx2csv /home/neha/Downloads/SVN.xlsx | awk -F ',' 'NR>1 {print $2}'))
output_file="svn_report.csv"

# loop over repositories and append output to CSV file
echo "Date,Revision,Author,Repo" > "$output_file"
for element in "${repo_links[@]}"
do
    repourl=$(echo $element | sed 's/"//')
    # Check if repository name starts with "http://"
    if [[ "$repourl" != http://* ]]; then
      # Add "http://" to the beginning of the repository name
      repourl="http://$repourl"
    fi
    echo "$repourl"
    log_data=$(svn log --quiet --xml --verbose -r "{${start_date}}:{${end_date}}" --username "$svn_username" --password "$svn_password" "$repourl")
    # Parse the log data to extract the relevant information
    dates=($(echo "$log_data" | grep -oP '<date>.*?</date>' | sed -e 's/<date>//g' -e 's/<\/date>//g'))
    revisions=($(echo "$log_data" | xmlstarlet sel -t -m "//logentry" -v "@revision" -n))
    authors=($(echo "$log_data" | grep -oP '<author>.*?</author>' | sed -e 's/<author>//g' -e 's/<\/author>//g'))    
    for (( i=0; i<${#dates[@]}; i++ ))
    do
      echo "${dates[i]},${revisions[i]},${authors[i]},$repourl" >> "$output_file"
    done
done
