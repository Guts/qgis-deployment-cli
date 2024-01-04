# import os
# import pwd
import getpass

# import win32net
# import win32security


srv_ldap_host = "svcldap"
srv_ldap_port = 389

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


from pyad import aduser

user = aduser.ADUser.from_cn(getpass.getuser())
print(user)
print(user.get_attribute("memberOf"))


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

# -- PURE WIN32COM
import win32com.client

objRootDSE = win32com.client.GetObject("LDAP://RootDSE")
objRootDSE.GetInfo()

for i in range(0, objRootDSE.PropertyCount - 1):
    prop = objRootDSE.Item(i)
    print(prop.Name)
    for val in prop.Values:
        print("  ", val.CaseIgnoreString)
