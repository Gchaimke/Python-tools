import asyncio
from functools import wraps, update_wrapper
import time


class TotalCounter:
    """Decorator class to count total calls to a function."""

    def __init__(self, func):
        update_wrapper(self, func)
        self.func = func
        self.total_calls = 0

    def __call__(self, *args, **kwargs):
        self.total_calls += 1
        print(f"Function {self.func.__name__!r} called {self.total_calls} times")
        return self.func(*args, **kwargs)


def timeit(func=None, *, print_results=False, is_async=False):
    """Decorator to measure execution time of async and regular functions."""
    def decorator_timeit(f):
        if is_async:
            @wraps(f)
            async def wrapper_timeit_async(*args, **kwargs):
                start_time = time.perf_counter()
                result = await f(*args, **kwargs)
                return _calculate_time(f, result, start_time)
            wrapper = wrapper_timeit_async
        else:
            @wraps(f)
            def wrapper_timeit(*args, **kwargs):
                start_time = time.perf_counter()
                result = f(*args, **kwargs)
                return _calculate_time(f, result, start_time)
            wrapper = wrapper_timeit

        def _calculate_time(func, result, start_time):
            if result and print_results:
                print("-----")
                print(result)
                print("-----")
            end_time = time.perf_counter()
            run_time = end_time - start_time
            print(f"Function {func.__name__!r} ready for {run_time:.4f} seconds")
            return result
        return wrapper

    # Case 1: The decorator was called without arguments, so the function is passed directly.
    if func is not None:
        return decorator_timeit(func)
    # Case 2: The decorator was called with arguments, so it returns the inner decorator.
    return decorator_timeit

@TotalCounter
async def fetch_something(index):
    """Simulate fetching data asynchronously."""
    await asyncio.sleep(1)
    print("Data received", index)
    return f'asset_{index}'


async def parse_something(asset):
    """Simulate parsing data asynchronously."""
    await asyncio.sleep(2)
    print("Data parsed for", asset)
    return f'parsed_{asset}'


@timeit(print_results=True, is_async=True)
async def run_all(items=5):
    """Run fetching and parsing tasks asynchronously."""
    fetch_results = await asyncio.gather(*[fetch_something(i) for i in range(items)])
    results = await asyncio.gather(*[parse_something(asset) for asset in fetch_results])
    return results


@timeit
def main():
    """
    Main function to run the async tasks.
    Runs the run_all function with 100 items.
    This will take approximately 3 seconds due to concurrent execution no matter 3 or 100 of items.
    1 second for fetching all items and 2 seconds for parsing all items.
    """
    asyncio.run(run_all(5))


if __name__ == "__main__":
    main()
