

# SUSE Manager Upgrade Scheduler

This is a simple Python script that connects to a SUSE Manager (SUMA) server and allows the user to schedule a package upgrade for a selected system. The script uses the `xmlrpc.client` library to communicate with the SUMA server and the `streamlit` library to create a web interface.


## Notes

- This script was developed and tested with SUSE Manager 4.2. It may not work with other versions of SUSE Manager.
- This script requires Python 3.6 or later.
- The `streamlit` library is used to create the web interface. If you prefer a different web framework, you can modify the code to use a different library.

## Requirements

- Python 3.6 or later
- Streamlit library
- xmlrpc.client library
- A SUSE Manager Server with a registered system

## Installation

1. Install Python 3.6 or later if not already installed
2. Install the Streamlit library by running `pip install streamlit`
3. Install the xmlrpc.client library by running `pip install xmlrpc.client`

## Usage

1. Update the connection parameters for the SUSE Manager Server in the code:

```python
MANAGER_URL = "https://10.0.0.20/rpc/api"
MANAGER_LOGIN = "sumaadmin"
MANAGER_PASSWORD = "exadmin"
```

2. Run the application by running `streamlit run app.py` in the command line
3. Select the target system and package from the dropdown menus
4. Click the "Upgrade" button to schedule the package upgrade for the selected system. A success message will be displayed if the upgrade is successful.




## Code Explanation

1. Import the necessary libraries:

```python
import streamlit as st
from xmlrpc.client import ServerProxy
import ssl
import datetime
```

2. Set up the connection parameters for the SUSE Manager Server:

```python
MANAGER_URL = "https://10.0.0.20/rpc/api"
MANAGER_LOGIN = "sumaadmin"
MANAGER_PASSWORD = "exadmin"
```

3. Define the `main()` function which is the entry point of the application:

```python
def main():
    """
    Main function to run the application.
    """
    # Create an SSL context to allow communication with the SUMA server
    context = ssl._create_unverified_context()

    # Create a connection to the SUMA server with the provided login credentials
    client = ServerProxy(MANAGER_URL, context=context)
    key = client.auth.login(MANAGER_LOGIN, MANAGER_PASSWORD)

    # Get a list of all active systems from the SUMA server
    activesystems = client.system.listActiveSystems(key)
    system_names = [system['name'] for system in activesystems]
    selected_system = st.selectbox('Select the target system:', system_names)

    # Get a list of upgradeable packages for the selected system
    system_id = [system['id'] for system in activesystems if system['name'] == selected_system][0]
    upgradeable_packages = client.system.listLatestUpgradablePackages(key, system_id)
    package_names = [package['name'] for package in upgradeable_packages]
    selected_package = st.selectbox('Select the package name:', package_names)

    if st.button('Upgrade'):
        # Schedule a package upgrade for the selected system
        scheduled_time = datetime.datetime.now()
        client.system.schedulePackageUpdate(key, [system_id], scheduled_time)
        st.success(f'Package {selected_package} has been successfully upgraded to {selected_system}!')
    else:
        st.warning('Please select a package and click the Upgrade button to upgrade it.')

    # Log out from the SUMA server
    client.auth.logout(key)
```

4. Define the condition to run the `main()` function when the script is executed:

```python
if __name__ == '__main__':
    main()
```