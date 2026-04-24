import asyncio
from backend.app.ai_pipeline import analyze_aspects

async def main():
    text = "The battery is good, but the screen is terrible. Also shipping was fast!"
    print(await analyze_aspects(text))

if __name__ == "__main__":
    asyncio.run(main())
