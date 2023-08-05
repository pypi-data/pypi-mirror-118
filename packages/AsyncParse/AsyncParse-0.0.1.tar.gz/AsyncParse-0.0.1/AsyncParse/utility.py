from collections import deque
import random



class ProxyCycle():  #Class needed to iterate through list of proxies

    def __init__(self, val: list):
        self.deque = deque(val)

    def __iter__(self):
        return self

    def __next__(self):
        if not self.deque:
            raise StopIteration
        item = self.deque.popleft()
        self.deque.append(item)
        return item
    
    def __bool__(self):
        return bool(list(self.deque))

    def delete_current(self):
        self.deque.popleft()


class Decorators():   #Error logging

    def exception_handler(original_func):
        def wrapper_func(*args, **kwargs):
            try:
                res = original_func(*args, **kwargs)
                return res
            except Exception as exc:
                print(str(exc))
        return wrapper_func


class HeadersManager():

    def __init__(self):
        self.user_agents = self.get_user_agents()

    def get_user_agents(self):
        with open("AsyncParse/user_agents.txt", "r") as file:
            agents = file.readlines()
            return [agent.strip() for agent in agents]
    
    @property
    def headers(self):
        random_user_agent = random.choice(self.user_agents)
        print(random_user_agent)
        return {
            "User-Agent": random_user_agent,
            "Accept": "application/json, text/plain, */*",
            "Referer": "https://www.kfc.ru/"
            }
