"""_summary_

Related hyperlinks:

- https://github.com/jcarswell/pyad/
- https://github.com/tjguk/wmi
- https://timgolden.me.uk/pywin32-docs/PyWin32.html
- https://mhammond.github.io/pywin32/html/com/help/active_directory.html
"""

# standard
import getpass
import os
import subprocess
from platform import uname

# 3rd party
import win32api
import win32com
import win32com.client
import win32net
import win32security

# import wmi

# user_info = win32net.NetUserGetInfo(
#     win32net.NetGetAnyDCName(), win32api.GetUserName(), 2
# )
# print(user_info)

domain = subprocess.run(
    ["powershell.exe", "(Get-CimInstance Win32_ComputerSystem).Domain"],
    stdout=subprocess.PIPE,
    text=True,
).stdout.strip()

print(domain)


# wmi_os = wmi.WMI().Win32_ComputerSystem()[0]
# print(wmi_os.Name, "PartOfDomain?", wmi_os.PartOfDomain)

# variables
srv_ldap_host = "svcldap"
srv_ldap_port = 389
PROTOCOL = "winmgmts:"


def construct_moniker():
    moniker = [PROTOCOL]
    return "".join(moniker)


# obj = win32com.client.GetObject("winmgmts:")
# print("obj: ", obj.IsClass)

# -- pywin32 (COM objects) : local groups
try:
    local_groups: list[str] = sorted(
        set(win32net.NetUserGetLocalGroups(uname()[1], getpass.getuser()))
    )
    print(f"User's local groups using pywin32: {'; '.join(local_groups)}")
except:
    print("no local groups retrieved")

# uid = os.getuid()
# user = pwd.getpwuid(uid)
# gl = os.getgrouplist(user.pw_name, user.pw_gid)
# print(gl)

# domain = None
# group_sid = win32security.LookupAccountName(domain, group_name)[0]


# import getpass
# import platform

# import win32net

# # Get current hostname and username
# sHostname = platform.uname()[1]
# sUsername = getpass.getuser()

# # Define account memberships to test as false
# memberAdmin = False
# memberORA_DBA = False

# print(win32net.NetUserGetLocalGroups(sHostname, sUsername))

# -- READ-AD

# import read_ad

# print(read_ad.get_first_user())
# my_user = read_ad.get_first_user(getpass.getuser())

# -- PYAD


import pyad

try:
    user = pyad.aduser.ADUser.from_cn(getpass.getuser())
    print(user.get_attribute("name")[0], user, type(user))
    print(user.get_domain())
    user_groups = user.get_memberOfs()
    for grp in user_groups:
        if not isinstance(grp, pyad.ADGroup):
            print("ARRRR")
        print(grp.get_group_scope())
        print(grp.get_attribute("name"))
    # print(user.get_attribute("memberOf"))
    print(len(user.get_memberOfs()) == len(user.get_attribute("memberOf")))
except Exception as err:
    print("Computer is not attached to any domain")


def is_computer_in_domain():
    try:
        # Connect to the WMI service
        wmi = win32com.client.GetObject("winmgmts://./root/cimv2")

        # Execute a query to retrieve information about the domain
        query = "SELECT * FROM Win32_ComputerSystem"
        result = wmi.ExecQuery(query)

        # Check if the domain attribute is not None
        for item in result:
            if item.Domain and item.Domain.lower() != "workgroup":
                return True

    except Exception as e:
        print(f"An error occurred: {e}")

    return False


print(is_computer_in_domain())

# # Connexion à Active Directory
# pyad.pyad_setdefaults(
#     ldap_server=srv_ldap_host
# )  # Remplacez "your_ldap_server" par l'adresse de votre serveur AD

# # Obtention de l'utilisateur courant
# # current_user = aduser.ADUser.from_cn(aduser.)

# # # Obtention de la liste des groupes auxquels l'utilisateur appartient
# # group_membership = current_user.get_attribute("memberOf")

# # # Affichage des groupes
# # print("Groupes auxquels l'utilisateur appartient:")
# # for group in group_membership:
# #     print(group)

# # -- PURE WIN32COM
# import win32com.client

# objRootDSE = win32com.client.GetObject("LDAP://RootDSE")
# objRootDSE.GetInfo()

# for i in range(0, objRootDSE.PropertyCount - 1):
#     prop = objRootDSE.Item(i)
#     print(prop.Name)
#     for val in prop.Values:
#         print("  ", val.CaseIgnoreString)
