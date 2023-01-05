# Create_hub_users_with_tokens

This is a short script to help ENGR131. This script will use the command line to create base users and hub user accounts for a jupyterhub. The script will mint a token and save the password and token to a csv.

To run the script with sudo access you type:

`python create_user_script.py file_name base_name number_of_accounts admin_api_token hub_ip_address`

where: 

`file_name` is the base filename for the CSV file

`base_name` is the base name of the user account <base_number>

`number_of_accounts` is the number of accounts to create. The accounts start at 1

`admin_api_token` is an api token associated with the admin account - this admin must be a sudoer

`hub_ip_address` is the ip address where the hub is located (This is just the address no http://)

To use:
1. clone the repository
2. Modify the batch.sh file if needed
3. `chmod +x ~/Create_hub_users_with_tokens/batch.sh`
4. `~/Create_hub_users_with_tokens/batch.sh {Admin API Token} {hub ip address}`