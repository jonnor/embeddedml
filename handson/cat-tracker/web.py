
import asyncio
from quart import Quart

app = Quart(__name__)


@app.route('/data', methods=['POST'])
async def post_data():
    return 'OK'


if __name__ == '__main__':
    asyncio.run(app.run_task())
