import asyncio
from typing import Optional

import uvicorn

from build.lib.clife_svc.errors.error_code import ParameterException
from clife_svc.application import App

app = App('clife_svc_test', '/www/logs')


async def detect(client_params: Optional[dict] = None) -> str:
    res = {'code': 0, 'msg': 'success'}
    # image_np = await app.get_img_np('http://cos.clife.net/10101/3cb34041583e4adebe241e8612d67eb2.png')
    # print(image_np)
    # res1 = await app.download_img('http://skintest.hetyj.com/ai/2R0FUj3S1630052673_28444.png')
    # print(res1)
    # await asyncio.sleep(3)
    # raise ParameterException()
    url = await app.upload_img('D:\\abc.xlsx')
    print(url)
    data = await app.download_img(url)
    print(data)
    return res

if __name__ == '__main__':
    app.add_api('/detect', detect, methods=['GET'])
    print(app.get_all_conf())
    loop = asyncio.get_event_loop()
    get_future = asyncio.ensure_future(app.download_img('http://skintest.hetyj.com/ai/WHbtvzo91630315253_abc.xlsx'))
    loop.run_until_complete(get_future)
    print(get_future.result())
    uvicorn.run(app.init_api(), host='0.0.0.0', port=30000, debug=True)
