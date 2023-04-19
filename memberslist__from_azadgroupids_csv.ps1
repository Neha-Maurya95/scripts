# Set the path to the CSV file containing the group IDs
$csvPath = "C:\groupsids.csv"

 

# Set the output path for the CSV file containing the group members
$outputPath = "C:\groupMembers.csv"

 

# Retrieve the group IDs from the CSV file
$groupIDs = Import-Csv -Path $csvPath | Select-Object -ExpandProperty ObjectId

 

# Create an empty array to store the group members
$groupMembers = @()

 

# Loop through each group ID and retrieve the members
foreach ($groupID in $groupIDs) {
   $group = Get-AzureADGroup -ObjectId $groupID
   $members = Get-AzureADGroupMember -ObjectId $groupID | Select-Object DisplayName, UserPrincipalName, ObjectType
   $members | ForEach-Object {
       $groupMembers += [PSCustomObject]@{
           GroupName = $group.DisplayName
           GroupID = $group.ObjectId
           DisplayName = $_.DisplayName
           UserPrincipalName = $_.UserPrincipalName
           ObjectType = $_.ObjectType
       }
   }
}

 

# Export the group members to a CSV file
$groupMembers | Export-Csv -Path $outputPath -NoTypeInformation
