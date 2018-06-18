Add-PSSnapIn Microsoft.HPC 
$j = New-HpcJob -Name 'Observer#0_2' -RequestedNodes 'CAGIS121,CAGIS122' -Exclusive $True 
$j | Add-HpcTask -WorkDir 'C:\Program Files' -Name 'Viewshed Task' -Type Basic -Command 'python \\CagisCondor\Viewshed\Scripts\viewshed_V2.py 0 2 3 C:\Viewshed\Input' 
$j | Submit-HpcJob  
$j = New-HpcJob -Name 'Observer#2_4' -RequestedNodes 'CAGIS121,CAGIS122' -Exclusive $True 
$j | Add-HpcTask -WorkDir 'C:\Program Files' -Name 'Viewshed Task' -Type Basic -Command 'python \\CagisCondor\Viewshed\Scripts\viewshed_V2.py 2 4 3 C:\Viewshed\Input' 
$j | Submit-HpcJob  
$j = New-HpcJob -Name 'Observer#4_5' -RequestedNodes 'CAGIS121,CAGIS122' -Exclusive $True 
$j | Add-HpcTask -WorkDir 'C:\Program Files' -Name 'Viewshed Task' -Type Basic -Command 'python C:\Viewshed\Scripts\viewshed_V2.py 4 5 3 C:\Viewshed\Input' 
$j | Submit-HpcJob  
