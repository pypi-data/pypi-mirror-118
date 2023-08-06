import discord
from discord.utils import get
from typing import List

from .modules.exceptions import *


class discord_advdb(object):

    def __init__(self, client, guild: discord.Guild, dbName: str = "database"):
        self.client = client
        self.guild = guild
        self.dbName = dbName
        self.db = discord.CategoryChannel

    async def getOrSetDB(self, overwrites: dict = None) -> int:
        """
        :param overwrites: a dict value, to overwrite to strict the database to players, be ware! If none
               everyone will be able to see the database, learn about PermissionOverwrites here:
               https://discordpy.readthedocs.io/en/rewrite/api.html#discord.PermissionOverwrite
        :return: the id of the newly created category, or the existing category id


        Notes:
            - Once you input overwrites into the function it'll update the current existing category's overwrites
              ( If overwrites is None it won't touch the database )
        """
        ctg = get(self.guild.categories, name=self.dbName)
        if ctg is None:
            ctg = await self.guild.create_category(name=self.dbName, overwrites=overwrites)
            self.db = ctg
            return ctg.id
        else:
            if not overwrites is None:
                for MorB in overwrites:  # MorB stands for Member Or Role
                    overwrite = overwrites.get(MorB)
                    await ctg.set_permissions(MorB, overwrite=overwrite)
            self.db = ctg
            return ctg.id

    async def setTable(self, tName: str, **columns: List[str]) -> int:
        """
        :param tName: The name of the table
        :param columns: the columns seperated by key-value, the value is a list of options for each column
        :return: the table Id

        NOTES:
        - if no table exists it'll raise an error stating Table Not Found
        - Only these options are acceptable at the moment: KEY, INT, STR, FLOAT
        - This is case-insensitive, not matter what you put it'll lower-case it so don't worry :)
        - If there will be no key column it'll raise an error stating there is no key column
        - Only one KEY column is allowed
        """
        table = get(self.db.text_channels, name=tName)
        tableDesc = "Columns:\n"
        if not table is None:
            raise TableAlreadyExists
        else:
            table = await self.db.create_text_channel(tName)
            await table.edit(sync_permissions=True)
        cList = list(columns.keys())
        for i in range(len(cList)):
            column = cList[i]
            options = columns.get(column)
            options = [x.upper() for x in options]

            if options.count("KEY") > 1 or options.count("INT") > 1 or options.count("STR") > 1 or options.count("FLOAT") > 1:
                raise OptionTypeError
            if options.count("INT") < 1 and options.count("STR") < 1 and options.count("FLOAT") < 1:
                raise EntryHasNoType

            for option in options:
                if option != "KEY" and option != "INT" and option != "STR" and option != "FLOAT":
                    options.remove(option)

            options = ','.join(options)
            if not i == len(cList) - 1:
                tableDesc += column + "[" + options + "], "
            else:
                tableDesc += column + "[" + options + "]"
        await table.edit(topic=tableDesc)
        return table.id

    def getTableId(self, tName: str) -> int:
        table = get(self.db.text_channels, name=tName)
        if table is None:
            raise TableDoesNotExist
        else:
            return table.id

    async def setEntry(self, tId: int, updateOnDuplicate: bool = False, *columnValues: list):
        """
        :param updateOnDuplicate: whether the value should be updated if the key is duplicated
        :param tId: the Id of the table
        :return: Nothing
        """
        for values in columnValues:
            keyColumns = []
            otherColumns = []
            table = get(self.db.text_channels, id=tId)
            if table is None:
                raise TableDoesNotExist(tId)
            columns = table.topic.split("\n")[1].split(", ")
            if len(columns) != len(values):
                raise NonEqualEntryException
            for i in range(len(columns)):
                column = columns[i]
                options = column.split("]")[0].split("[")[1].split(",")
                value = values[i]
                if "KEY" in options:
                    keyColumns.append(value)
                else:
                    otherColumns.append(value)
            entry_data = str(keyColumns).strip('[]').replace("'", "") + " : [ " + str(otherColumns).strip('[]').replace(
                "'", "") + " ] "
            messages = await table.history().flatten()
            msg = discord.Message
            for message in messages:
                keyValue = message.content.split(":")
                if str(keyColumns).strip('[]').replace("'", "") in keyValue[0]:
                    if updateOnDuplicate:
                        msg = message
                        break
                    else:
                        raise KeyAlreadyExists
            if not msg is discord.Message:
                await msg.edit(content=entry_data)
            else:
                await table.send(entry_data)

    async def getEntry(self, tId: int, *keys: str):
        """
        :param tId: the table Id
        :param keys: the keys to get the data off
        :return: Hashmap of the data for easy access with the keys you want to work with :)
        """
        entry_data = {}
        table = get(self.db.text_channels, id=tId)
        if len(keys) != 0:
            async for msg in table.history():
                if msg.author.bot:
                    content = msg.content.split(" : ")
                    if [content[0]] in keys:
                        entry_data[content[0]] = content[1]
        return entry_data
