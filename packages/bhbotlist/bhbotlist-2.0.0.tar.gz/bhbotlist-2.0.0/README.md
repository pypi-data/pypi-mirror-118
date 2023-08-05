# bhbotlist 
useful library for [bhbotlist.xyz](https://bhbotlist.xyz)

## Installation
```
pip install bhbotlist
```
## example 
Server Count Post :
```python
from bhbotlist import bhbotlist
from discord.ext import commands

client = commands.Bot(command_prefix="!") 
dbl = bhbotlist(client,"token of bhbotlist")

@client.event
async def on_ready():
  x = await dbl.serverCountPost()
  print(x)

client.run("token")
```
