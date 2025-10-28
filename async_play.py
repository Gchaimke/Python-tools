import asyncio
import aiohttp

URLS = ['https://www.python.org', 'https://www.google.com',
        'https://non-existent-domain-12345.org']


async def countdown(name, delay):
    print(f"Запуск таймера {name} на {delay} секунд")
    for i in range(delay, 0, -1):
        print(f"{name}: {i} секунд осталось")
        await asyncio.sleep(1)
    print(f"Таймер {name} завершен")


async def racer(name, delay):
    await asyncio.sleep(delay)
    print(f"{name} финишировал после {delay} секунд")


async def check_status(url):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    print(f"{url}: OK")
                else:
                    print(
                        f"{url}: Не удалось подключиться, статус {response.status}")
    except Exception as e:
        print(f"{url}: недоступен: {e}")


async def long_running_task():
    print("Фоновая задача начала работу...")
    await asyncio.sleep(3)
    print("Фоновая задача завершена")


async def coock():
    async def prepare_ingredients():
        print("Подготовка ингредиентов...")
        await asyncio.sleep(2)
        print("Ингредиенты готовы.")

    async def fry_meat():
        print("Жарка мяса...")
        await asyncio.sleep(3)
        print("Мясо жарено.")

    async def boil_rice():
        print("Варка риса...")
        await asyncio.sleep(4)
        print("Рис сварен.")

    print("Starting coock...")
    start_time = asyncio.get_event_loop().time()
    await prepare_ingredients()
    await asyncio.gather(fry_meat(), boil_rice())
    end_time = asyncio.get_event_loop().time()
    print(f"Coock finished in {end_time - start_time} seconds.")


async def main(run_func='coock'):
    match run_func:
        case 'coock':
            await coock()
        case 'long_task':
            task = asyncio.create_task(long_running_task())
            print("Основная программа продолжает работу...")
            count = 5
            while count > 0:
                print(f"Фоновая задача выполнена: {task.done()}")
                print("Основная программа работает...")
                await asyncio.sleep(1)
                count -= 1
            await task
            print("Основная программа завершена.")

        case 'check_status':
            await asyncio.gather(*[check_status(url) for url in URLS])
        case 'racer':
            await asyncio.gather(
                racer("Гонщик 1", 3),
                racer("Гонщик 2", 5),
                racer("Гонщик 3", 2),
            )
        case 'countdown':
            await asyncio.gather(countdown('timer 1', 5), countdown('timer 2', 3))

if __name__ == "__main__":
    asyncio.run(main())
