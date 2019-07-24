# cgxCopyMGMT

WARNING: USE AT YOUR OWN RISK

Copy Device Management Policy from one interface to anotehr

Instructions:

* Install python3
* Install cloudgenix python sdk : pip3 install cloudgenix
* Setup authentication as listed below
* Create a csv file with the example at t_list.csv
* run the script using: python3 cgxCopyMGMT.py --s_element "source claimed device name" --s_interface "source interface to copy from" --interfaces_file "file with a list of target itnerface to paste to"
* You can also specify one target with the --t_element and --t_interface 

cgxCopyMGMT.py looks for the following for AUTH, in this order of precedence:

* --email or --password options on the command line.
* CLOUDGENIX_USER and CLOUDGENIX_PASSWORD values imported from cloudgenix_settings.py
* CLOUDGENIX_AUTH_TOKEN value imported from cloudgenix_settings.py
* X_AUTH_TOKEN environment variable
* AUTH_TOKEN environment variable
* Interactive prompt for user/pass (if one is set, or all other methods fail.)

Exmpale:
```
bash:cgxCopyMGMT dan$ ./cgxCopyMGMT.py --s_element "Dan 2k" --s_interface "1" --interfaces_file t_list.csv 
INFO:cgxCopyMGMT:Copy to interface 3 of elementDan 2k
INFO:cgxCopyMGMT:------ Deleting existing Device Management configuration from the interface
INFO:cgxCopyMGMT:----- Success
INFO:cgxCopyMGMT:Copy to interface 14 of elementDC Device
INFO:cgxCopyMGMT:------ Deleting existing Device Management configuration from the interface
INFO:cgxCopyMGMT:----- Success
INFO:cgxCopyMGMT:Copy to interface 13 of elementDC Device
INFO:cgxCopyMGMT:----- Success
```

Example of "interfaces file":
```
Dan 2k,3
DC Device,14
```

Example using explicit target:
```
bash:cgxCopyMGMT dan$ ./cgxCopyMGMT.py --s_element "Dan 2k" --s_interface "1" --t_element "DC Device" --t_interface "14"                    
INFO:cgxCopyMGMT:Copy to interface 14 of elementDC Device
INFO:cgxCopyMGMT:----- Success
```