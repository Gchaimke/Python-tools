import asyncio
import aiohttp

URLS = ['https://www.python.org', 'https://www.google.com',
        'https://non-existent-domain-12345.org']


async def countdown(name, delay):
    print(f"Start timer {name} with {delay} seconds")
    for i in range(delay, 0, -1):
        print(f"{name}: {i} seconds left")
        await asyncio.sleep(1)
    print(f"Timer {name} finished")


async def racer(name, delay):
    await asyncio.sleep(delay)
    print(f"{name} finished after {delay} seconds")


async def check_status(url):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    print(f"{url}: OK")
                else:
                    print(
                        f"{url}: Connection failed, status {response.status}")
    except Exception as e:
        print(f"{url}: Unreachable: {e}")


async def long_running_task():
    print("Background task started...")
    await asyncio.sleep(3)
    print("Background task finished...")


async def cook():
    async def prepare_ingredients():
        print("Preparing ingredients...")
        await asyncio.sleep(2)
        print("Ingredients ready.")

    async def fry_meat():
        print("Frying meat...")
        await asyncio.sleep(3)
        print("Meat fried.")

    async def boil_rice():
        print("Boiling rice...")
        await asyncio.sleep(4)
        print("Rice boiled.")

    print("Starting cook...")
    start_time = asyncio.get_event_loop().time()
    await prepare_ingredients()
    await asyncio.gather(fry_meat(), boil_rice())
    end_time = asyncio.get_event_loop().time()
    print(f"Cook finished in {end_time - start_time} seconds.")


async def main(run_func='cook'):
    match run_func:
        case 'cook':
            await cook()
        case 'long_task':
            task = asyncio.create_task(long_running_task())
            print("Main program is running...")
            count = 5
            while count > 0:
                print(f"Background task is done: {task.done()}")
                print("Main program is working...")
                await asyncio.sleep(1)
                count -= 1
            await task
            print("Main program finished.")

        case 'check_status':
            await asyncio.gather(*[check_status(url) for url in URLS])
        case 'racer':
            await asyncio.gather(
                racer("Racer 1", 3),
                racer("Racer 2", 5),
                racer("Racer 3", 2),
            )
        case 'countdown':
            await asyncio.gather(countdown('timer 1', 5), countdown('timer 2', 3))

if __name__ == "__main__":
    asyncio.run(main())
