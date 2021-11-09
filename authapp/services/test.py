from authapp.services.debugger import time_of_function
import time
import asyncio

async def create_notification():
    print('start create')
    print('create complete')

async def send_email():
    print('start send_mail')
    await asyncio.sleep(0)
    print('send_mail complete')

@time_of_function
def send():
    create_notification()
    send_email()

ioloop = asyncio.get_event_loop()
tasks = [ioloop.create_task(create_notification()), ioloop.create_task(send_email())]
wait_tasks = asyncio.wait(tasks)
ioloop.run_until_complete(wait_tasks)
ioloop.close()



send()

