# import os
# import pwd

# import win32net
# import win32security

# uid = os.getuid()
# user = pwd.getpwuid(uid)
# gl = os.getgrouplist(user.pw_name, user.pw_gid)
# print(gl)

# domain = None
# group_sid = win32security.LookupAccountName(domain, group_name)[0]


import getpass
import platform

import win32net

# Get current hostname and username
sHostname = platform.uname()[1]
sUsername = getpass.getuser()

# Define account memberships to test as false
memberAdmin = False
memberORA_DBA = False

print(win32net.NetUserGetLocalGroups(sHostname, sUsername))
