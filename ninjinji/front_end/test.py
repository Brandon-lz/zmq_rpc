from concurrent.futures import ThreadPoolExecutor
from time import sleep
def task(message):
    print("to do "+message)
    sleep(2)
    return message
def main():
    executor = ThreadPoolExecutor(5)
    future = executor.submit(task, ("Completed"))     # 开始执行任务
    # print(future.done())
    # sleep(3)
    # print(future.done())
    # print(future.result())
    sleep(5)
if __name__ == '__main__':
    main()