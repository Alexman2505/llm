import asyncio
import httpx
from agno.agent import Agent
from agno.models.ollama import Ollama


async def get_weather(city: str) -> str:
    """Получает текущую погоду через wttr.in (бесплатно, без ключа)"""
    url = f"https://wttr.in/{city}?format=%t+%h+%w+%C"
    # %t - температура, %h - влажность, %w - ветер, %C - описание

    async with httpx.AsyncClient() as client:
        response = await client.get(url, timeout=10)
        data = response.text.strip()
        # wttr.in возвращает что-то вроде: "+25°C 60% 15 km/h Sunny"

        parts = data.split()
        if len(parts) >= 4:
            temp = parts[0].replace('+', '').replace('°C', '')
            humidity = parts[1].replace('%', '')
            wind = parts[2]
            condition = ' '.join(parts[3:])
            return (
                f"{temp}°C, влажность {humidity}%, ветер {wind}, {condition}"
            )
        return data


agent = Agent(
    name="Погодный помощник",
    model=Ollama(id="llama3.2:3b"),
    tools=[get_weather],
    instructions=[
        "Ты помощник, умеющий узнавать погоду через функцию get_weather",
        "Всегда вызывай get_weather для получения актуальных данных",
        "Отвечай кратко и на русском языке",
        "Если пользователь не указал город, спроси его",
    ],
)


async def main():
    print("🤖 Погодный агент запущен!\n")
    while True:
        user_input = input("👉 Вы: ")
        if user_input.lower() in ["выход", "exit", "quit"]:
            break
        response = await agent.arun(user_input)
        print(f"🤖 {response.content}\n")


if __name__ == "__main__":
    asyncio.run(main())
