import win32api
import win32net
import win32netcon
import win32security

server = None


def ServerEnum():
    "Enumerates all servers on the network"
    resume = 0
    server = None

    while 1:
        data, total, resume = win32net.NetServerEnum(
            server, 100, win32netcon.SV_TYPE_ALL, None, resume
        )
        for s in data:
            print("Found server %s" % s["name"])
            # Now loop over the shares.
            shareresume = 0
            while 1:
                sharedata, total, shareresume = win32net.NetShareEnum(
                    server, 2, shareresume
                )
                for share in sharedata:
                    print(
                        " %(netname)s (%(path)s):%(remark)s - in use by %(current_uses)d users"
                        % share
                    )
                if not shareresume:
                    break
        if not resume:
            break
    print("Enumerated all the servers on the network")


def GetInfo(userName=None):
    "Dumps level 3 information about the current user"
    if userName is None:
        userName = win32api.GetUserName()
    print(f"Dumping level 3 information about user: {userName}")
    info = win32net.NetUserGetInfo(None, userName, 3)
    for key, val in info.items():
        print("%s=%s" % (key, val))


def LocalGroupEnum():
    "Enumerates all the local groups"
    resume = 0
    nmembers = 0
    server = None

    data, total, resume = win32net.NetLocalGroupEnum(server, 1, resume)
    for group in data:
        print("\n\tFound group: %(name)s " % group)
        memberresume = 0
    print(group.keys())
    #     while 1:
    #         memberdata, total, memberresume = win32net.NetLocalGroupGetMembers(server, group['name'], 2, resume)
    #         for member in memberdata:
    #             # Just for the sake of it, we convert the SID to a username
    #             username, domain, type = win32security.LookupAccountSid(server, member['sid'])
    #             nmembers = nmembers + 1
    #             print(" Member %s (%s)" % (username, member['domainandname']))
    #         if memberresume==0:
    #             break
    # if not resume:
    #     break
    assert nmembers, "Couldnt find a single member in a single group!"
    print("Enumerated all the local groups")


def GroupEnum():
    "Enumerates all the domain groups"
    nmembers = 0
    resume = 0
    server = win32api.GetDomainName()

    while 1:
        data, total, resume = win32net.NetGroupEnum(server, 1, resume)
        #               print "Call to NetGroupEnum obtained %d entries of %d total" % (len(data), total)
        for group in data:
            print("Found group %(name)s:%(comment)s " % group)
            memberresume = 0
            while 1:
                memberdata, total, memberresume = win32net.NetGroupGetUsers(
                    server, group["name"], 0, resume
                )
                for member in memberdata:
                    # print(" Member %(name)s" % member)
                    nmembers = nmembers + 1
                if memberresume == 0:
                    break
        if not resume:
            break
    assert nmembers, "Couldnt find a single member in a single group!"
    print("Enumerated all the groups")


print(win32api.GetDomainName())

# print(GetInfo())
# ServerEnum()
# LocalGroupEnum()
GroupEnum()
