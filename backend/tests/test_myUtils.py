import asyncio

import pytest
from api.mySchemas import MyTimeoutError
from api.myUtils import monitor


@pytest.mark.asyncio
async def test_monitor():
    async def _test_monitor(countdown: int):
        while countdown > 0:
            countdown -= 1
            print(countdown)
            await asyncio.sleep(1)

    with pytest.raises(MyTimeoutError) as error:
        await monitor(_test_monitor(16))
    assert str(error.value) == "Time limit exceeded"
    try:
        await monitor(_test_monitor(14))
    except Exception as err:
        pytest.fail(f"Unexpected exception raised: {err}")
