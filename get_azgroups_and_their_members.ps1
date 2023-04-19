$groups = Get-AzureADGroup -All $true
$report = Foreach ($group in $groups) {
  $users = $group | Get-AzureADGroupMember
  # create output objects with username and groups:
  Foreach ($user in $users) {
    [PSCustomObject][ordered]@{ 
      GroupDisplayName  = $group.DisplayName
      UserDisplayName   = $user.DisplayName
      UserPrincipalName = $user.UserPrincipalName

}}}
$report | Export-CSV -Path "C:\get_azgroups_and_their_users.csv"