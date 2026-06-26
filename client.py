import asyncio
from dotenv import load_dotenv
from anthropic import AsyncAnthropic

load_dotenv()
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp.client.session import RequestContext
from mcp.types import (
    CreateMessageRequestParams,
    CreateMessageResult,
    TextContent,
    SamplingMessage,
)

anthropic_client = AsyncAnthropic()
model = "claude-sonnet-4-6"

server_params = StdioServerParameters(
    command="uv",
    args=["run", "server.py"],
)


async def chat(input_messages: list[SamplingMessage], max_tokens=4000):
    messages = []
    for msg in input_messages:
        if msg.role == "user" and msg.content.type == "text":
            content = (
                msg.content.text
                if hasattr(msg.content, "text")
                else str(msg.content)
            )
            messages.append({"role": "user", "content": content})
        elif msg.role == "assistant" and msg.content.type == "text":
            content = (
                msg.content.text
                if hasattr(msg.content, "text")
                else str(msg.content)
            )
            messages.append({"role": "assistant", "content": content})

    response = await anthropic_client.messages.create(
        model=model,
        messages=messages,
        max_tokens=max_tokens,
    )

    text = "".join([p.text for p in response.content if p.type == "text"])
    return text


async def sampling_callback(
    context: RequestContext, params: CreateMessageRequestParams
):
    # Call Claude using the Anthropic SDK
    text = await chat(params.messages)

    return CreateMessageResult(
        role="assistant",
        model=model,
        content=TextContent(type="text", text=text),
    )


async def run():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(
            read, write, sampling_callback=sampling_callback
        ) as session:
            await session.initialize()

            result = await session.call_tool(
                name="summarize",
                arguments={"text_to_summarize": """f
                Flowers, also known as blossoms and blooms, are the reproductive structures of flowering plants. Typically, they are structured in four circular levels around the end of a stalk. These include: sepals, which are modified leaves that support the flower; petals, often designed to attract pollinators; male stamens, where pollen is presented; and female gynoecia, where pollen is received and its movement is facilitated to the egg. When flowers are arranged in a group, they are known collectively as an inflorescence.

                The development of flowers is a complex and important part in the life cycles of flowering plants. In most plants, flowers are able to produce sex cells of both sexes. Pollen, which can produce the male sex cells, is transported between the male and female parts of flowers in pollination. Pollination can occur between different plants, as in cross-pollination, or between flowers on the same plant or even the same flower, as in self-pollination. Pollen movement may be caused by animals, such as birds and insects, or non-living things like wind and water. The colour and structure of flowers assist in the pollination process.
                """},
            )
            print(result.content)


if __name__ == "__main__":
    import asyncio

    asyncio.run(run())
