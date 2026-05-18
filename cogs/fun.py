import logging
import random

import aiohttp
from discord.ext import commands


class Fun(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.session = aiohttp.ClientSession()

    async def cog_unload(self):
        await self.session.close()

    async def _fetch_from_api(
        self, ctx, url: str, response_handler, error_message: str
    ):
        try:
            async with self.session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    await response_handler(ctx, data)
                else:
                    logging.warning(
                        msg=f"{error_message} request failed with status: {response.status}"
                    )
        except aiohttp.ClientError as e:
            logging.error(msg=f"Error fetching {error_message}: {e}")

    async def _meme_handler(self, ctx, data):
        await ctx.send(data["url"])

    @commands.command()
    async def meme(self, ctx):
        await self._fetch_from_api(
            ctx,
            url="https://meme-api.com/gimme",
            response_handler=self._meme_handler,
            error_message="Meme API",
        )

    async def _joke_handler(self, ctx, data):
        if data["type"] == "single":
            await ctx.send(data["joke"])
        elif data["type"] == "twopart":
            await ctx.send(data["setup"])
            await ctx.send(data["delivery"])

    @commands.command()
    async def joke(self, ctx) -> None:
        await self._fetch_from_api(
            ctx,
            url="https://v2.jokeapi.dev/joke/Any?blacklistFlags=nsfw,religious,political,racist,sexist,explicit",
            response_handler=self._joke_handler,
            error_message="Joke API",
        )

    async def _fact_handler(self, ctx, data):
        await ctx.send(data["text"])

    @commands.command()
    async def fact(self, ctx) -> None:
        await self._fetch_from_api(
            ctx,
            url="https://api.viewbits.com/v1/uselessfacts?mode=random",
            response_handler=self._fact_handler,
            error_message="fact api",
        )

    @commands.command()
    async def ping(self, ctx) -> None:
        await ctx.send("pong!")

    @commands.command()
    async def roll(self, ctx, sides: int = 6) -> None:
        """Rolls a die with a specified number of sides."""
        result: int = random.randint(a=1, b=sides)
        await ctx.send(f"{result} 🎲")

    @commands.command()
    async def ball(self, ctx) -> None:
        answers: list[str] = ["No", "Maybe", "idk", "Yes", "Probably... Not"]
        answer: str = random.choice(seq=answers)
        await ctx.send(f"{answer} ")


async def setup(bot):
    await bot.add_cog(Fun(bot))
