import asyncio

import pytest
from api.my_schemas import MyTimeoutError
from api.my_utils import MAX_DURATION, monitor


@pytest.mark.asyncio
async def test_monitor():
    async def _test_monitor(countdown: int):
        while countdown > 0:
            countdown -= 1
            print(countdown)
            await asyncio.sleep(1)

    with pytest.raises(MyTimeoutError) as error:
        await monitor(_test_monitor(MAX_DURATION))
    assert str(error.value) == "Time limit exceeded"
    try:
        await monitor(_test_monitor(1))
    except Exception as err:
        pytest.fail(f"Unexpected exception raised: {err}")
