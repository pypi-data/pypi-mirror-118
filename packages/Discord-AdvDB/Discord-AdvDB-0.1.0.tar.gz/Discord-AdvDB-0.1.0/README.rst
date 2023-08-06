=============
Discord-AdvDB
=============


.. image:: https://img.shields.io/pypi/v/discord_advdb.svg
        :target: https://pypi.python.org/pypi/discord_advdb

Advanced Database in discord


* Free software: GNU General Public License v3
* Documentation: https://discord-advdb.readthedocs.io.


Installation
-------
In order to use it first thing you have to do is install the package like this in your terminal:
```sh
pip install Discord-AdvDB
```

Commands
-------

* getOrSetDB: gets the Database ( Category ) or setting a new one according to what you've set in the configuration method ( see example below )
    Notes:
            - Once you input overwrites into the function it'll update the current existing category's overwrites
              ( If overwrites is None it won't touch the database )
* SetTable: Sets a new table according to the information, the required information is a the table name and key-value type of columns ( ```python3 reading=["KEY", "STR"] )
    NOTES:
        - if table exists it'll raise an error stating Table Found
        - Only these options are acceptable at the moment: KEY, INT, STR, FLOAT
        - This is case-insensitive, not matter what you put it'll lower-case it so don't worry :)
        - If there will be no key column it'll raise an error stating there is no key column
        - Only one KEY column is allowed

* getTableId: gets the table id incase you need it ( You won't need for the database cause it's already in the code, this category is the object )
* setEntry: setting a new entry/ies, you can select if you want existing keys to update and the column values
    NOTES:
        - The column values is the list of the values from the table ( MUST BE IN COLUMN ORDER )O
* getEntry: returns a hash map of the key and it's value ( It returns in hashmap to read it easier in code )


Example
-------
NOTE: the example is from a cog file
```python
import discord
from discord.ext import commands
from discord.utils import get
import discord_advdb.discord_advdb as DB

global DiscordAdvDB


class events(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        global DiscordAdvDB
        print("Bot is ready!")
        for guild in self.client.guilds:
            DiscordAdvDB = DB.discord_advdb(self.client, guild, "database")

    @commands.command()
    async def test(self, ctx):
        guild = ctx.message.guild
        db = await DiscordAdvDB.getOrSetDB({
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            guild.me: discord.PermissionOverwrite(read_messages=True)
        })
        tableId = await DiscordAdvDB.setTable("test1",
                                              reading=["KEY", "STR"],allowing=["INT"])
        tbId = DiscordAdvDB.getTableId("test1")
        await DiscordAdvDB.setEntry(tbId, True, [8, 6], ["Hey", 9000])
        print(await DiscordAdvDB.getEntry(tbId, ["8"]))```



Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
