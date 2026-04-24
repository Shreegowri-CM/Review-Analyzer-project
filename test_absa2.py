import asyncio
from backend.app.ai_pipeline import analyze_aspects

async def main():
    text = "battery is good quality is bad and delivery was on time"
    print(await analyze_aspects(text))

if __name__ == "__main__":
    asyncio.run(main())
