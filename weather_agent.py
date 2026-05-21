import asyncio
from agno.agent import Agent
from agno.models.ollama import Ollama
import python_weather


async def get_weather(city: str) -> str:
    """Получает текущую погоду в городе."""
    async with python_weather.Client() as client:
        weather = await client.get(city)
        return (
            f"{weather.temperature}°C, ощущается как {weather.feels_like}°C. "
            f"{weather.description}. Влажность: {weather.humidity}%"
        )


agent = Agent(
    name="Погодный помощник",
    model=Ollama(id="llama3.2:3b"),  # Замените на вашу модель
    tools=[get_weather],
    instructions=[
        "Ты помощник, умеющий узнавать погоду через функцию get_weather",
        "Если спрашивают про погоду — ОБЯЗАТЕЛЬНО вызови get_weather",
        "Никогда не выдумывай погоду",
        "Отвечай коротко и на русском",
    ],
)


async def main():
    print("🤖 Агент запущен. Задайте вопрос о погоде:\n")

    while True:
        user_input = input("👉 Вы: ")
        if user_input.lower() in ["выход", "exit"]:
            break

        response = await agent.arun(user_input)
        print(f"\n🤖 {response.content}\n")


if __name__ == "__main__":
    asyncio.run(main())
