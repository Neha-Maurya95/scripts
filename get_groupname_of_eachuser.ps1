$users = Get-AzureADUser -All $true

$report = Foreach ($user in $users) {
  $groups = $user | Get-AzureADUserMembership

  # create output objects with username and groups:
  Foreach ($group in $groups) {
    [PSCustomObject][ordered]@{ 
      UserDisplayName   = $user.DisplayName
      UserPrincipalName = $user.UserPrincipalName
      GroupDisplayName  = $group.DisplayName
}}}

# print a table with desired formatting
$report | Export-CSV -Path "C:\get_azusers_and_their_groups.csv"


  
