# Sysblock

A systemwide ad/tracker/malware/crypto blocker for windows and linux. 
_In other words: A sophisticated application decrapifier._

## Features
**Convenience**

A one step install with default presets: (uses oisd's reliable blocklist)

Manual config (easy to use) configuration of your host file: Add a custom blocklist through its link, whitelist/blacklist domains

## How is this achieved?

Every os has a host file which was used to map ip's with their correlating domain, which was mainly used before dns was introduced, because host comes before the dns, it can make for a great systemwide content blocker as instead of for e.g correlating ad.com with its ip (192...) it'd be correlated with a "dummy ip" such as localhost (127.168.0.0) or 0.0.0.0 which wont load the domain. Which is the purpose of sysblock, a sophisticated yet easy to use tool to manage your host file as an content blocker.
