import streamlit as st
from xmlrpc.client import ServerProxy
import ssl
import datetime

# Set up connection parameters for the SUMA server
MANAGER_URL = "https://10.0.0.20/rpc/api"
MANAGER_LOGIN = "sumaadmin"
MANAGER_PASSWORD = "exadmin"


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
        # Upgrade the specified package to the target system
        client.system.schedulePackageUpdate(key, [system_id], datetime.datetime.now().isoformat())
        st.success(f'Package {selected_package} has been successfully upgraded to {selected_system}!')
    else:
        st.warning('Please select a package and click the Upgrade button to upgrade it.')

    # Log out from the SUMA server
    client.auth.logout(key)


if __name__ == '__main__':
    main()