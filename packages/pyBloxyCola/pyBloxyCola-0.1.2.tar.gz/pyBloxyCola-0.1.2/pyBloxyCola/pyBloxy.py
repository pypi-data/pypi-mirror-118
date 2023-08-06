import requests

class pyBloxyCola(object):
    """
    Sadly done with the requests package, maybe will change in the feature
    This is a easy project but I find it fun to make.
    """

    def getUserInJSON(self, userid):
        """
            Grabs UserInfo via ID and putting it in a JSON.
        """
        return requests.get("https://users.roblox.com/v1/users/{}".format(userid)).json()

    def isUserBanned(self, userid):
        """
            Grabs ID and returns false is not banned and True is banned.
        """
        return requests.get("https://users.roblox.com/v1/users/{}".format(userid)).json()['isBanned']


    def getGroupInfoInJSON(self, groupid):
        """
            Grabs Group ID and returns the data in JSON.
        """
        return requests.get("https://groups.roblox.com/v2/groups?groupIds={}".format(groupid)).json()