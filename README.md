# scripts

#### 1. Python script to extract the Revision, Repo, Date, Author, Comment , Action and path files on which the action is took place for svn repos.SVN repos are listed in CSV file as below given format, it collect the data from log entries :
The format of csv file of repos 
| Repository | Repository Links   |
| :---:      |    :---:           | 
| Abc        | (http://192.168.10.15/svn/Abc)                | 

| command    |
| :---:      | 
| $ python3 svn_completelogs_script.py |

#### 2. Python script to the Revision, Repo, Date, Author, Comment , Action and path files on which the action is took place for single svn repo added as array. (you can more repos to that array). it collect the data from log entries :
The format of csv file of repos 

| command    |
| :---:      | 
| $ python3 single-svnrepo-report.py |


#### 3. Bash script to get python script to extract the Revision, Repo, Date, Author of svn repos. it collect the data from log entrie

| command    |
| :---:      | 
| $ bash svn-report.sh |

#### 4. Powershell script to get members of azure active directory groups. The group ids are listed in .csv file.
[ Notes : your .csv file should be having group's Object ID's , you can use the below command to get the group ids in csv file and then use that csv file in your script]

| command    |
| :---:      | 
| $ ./memberslist__from_azadgroupids_csv.ps1 |


  
