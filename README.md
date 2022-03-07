# Sysblock
A systemwide ad/tracker/malware/crypto blocker for windows and linux. 
_In other words: A sophisticated application decrapifier._

## How is this achieved?

Every os has a host file which was used to map ip's with their correlating domain, this was mainly used before dns was introduced, because host comes before the dns, it can make for a great systemwide content blocker which for e.g, instead of correlating ad.com with its ip it'd be correlated with a "dummy ip" such as 0.0.0.0 which wont load the domain. Which is the purpose of sysblock, a sophisticated yet easy to use tool to manage your host file as an content blocker.

### Todo:

* [x] Windows support
* [x] Linux support
* [ ] whitelisting capability
* [x] blacklisting capability
* [x] custom redirects
* [x] Download via url

## Limitations

* As with any hosts/dns based adblock, whilst useful for being system wide, it wont have as complex rules as html filtering browser based extensions as it solely uses domains. For best results, you can combine sysblock with the ublock origin extension
* It cannot block youtube ads, you may want to use invidious for this.
