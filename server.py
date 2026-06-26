import asyncio
from mcp.server.fastmcp import FastMCP, Context
from mcp.types import SamplingMessage, TextContent

mcp = FastMCP(name="Demo Server")


@mcp.tool()
async def summarize(text_to_summarize: str, ctx: Context):
    await ctx.info("Starting summarization...")
    await ctx.report_progress(20, 100)
    await asyncio.sleep(2)

    prompt = f"""
        Please summarize the following text:
        {text_to_summarize}
    """

    await ctx.info("Sending request to LLM via sampling...")
    await ctx.report_progress(50, 100)
    await asyncio.sleep(1)

    result = await ctx.session.create_message(
        messages=[
            SamplingMessage(
                role="user", content=TextContent(type="text", text=prompt)
            )
        ],
        max_tokens=4000,
        system_prompt="You are a helpful research assistant.",
    )

    await asyncio.sleep(3)
    await ctx.info("Summarization complete.")
    await ctx.report_progress(100, 100)

    if result.content.type == "text":
        return result.content.text
    else:
        raise ValueError("Sampling failed")


if __name__ == "__main__":
    mcp.run(transport="stdio")
