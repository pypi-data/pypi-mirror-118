import sys
import os
import json
import httpx
import asyncio
from urllib.parse import urljoin
from typing import Dict, List, Optional
from pydantic import BaseModel
from rich import print
from rich import console
from rich.table import Table
from rich.console import Console
from datetime import datetime, timedelta
from pytz import timezone
from os import system
import time


class ClokifyNewEntry(BaseModel):
    start: str
    end: str = None
    billable: bool = False
    projectId: str
    taskId: str
    duration: str = None
    description: str = ""


CONFIG_DIR = os.path.join(
    os.path.expanduser("~"),
    ".config/clokipy"
)
BASE_API_URL = "https://api.clockify.me/api/v1/"
CACHE = {}

console = Console()


async def Get(url: str,
              params: Optional[Dict] = {},
              headers: Optional[Dict] = {},
              timeout: int = 10,
              request_title: str = "Making Request",
              multiple: bool = False,
              apikey: str = ""):

    headers = {
        **headers,
        'X-Api-Key': apikey,
        "Content-Type": "application/json"
    }

    async with httpx.AsyncClient() as client:

        try:

            if multiple is False:

                with console.status(request_title) as status:
                    response = await client.get(url=url, params=params, headers=headers, timeout=timeout)

                    return response
            else:
                response = await client.get(url=url, params=params, headers=headers, timeout=timeout)
                return response

        except Exception as e:
            print(e)
            return False


async def Path(url: str,
               params: Optional[Dict] = {},
               data: Dict = {},
               headers: Optional[Dict] = {},
               timeout: int = 10,
               request_title: str = "Making Request",
               apikey: str = ""):

    headers = {
        **headers,
        'X-Api-Key': apikey,
        "Content-Type": "application/json"
    }
    async with httpx.AsyncClient() as client:

        try:
            with console.status(request_title) as status:
                response = await client.patch(url=url, params=params, headers=headers, timeout=timeout, data=data)

                return response

        except Exception as e:
            return False


async def Put(url: str,
              params: Optional[Dict] = {},
              data: Dict = {},
              headers: Optional[Dict] = {},
              timeout: int = 10,
              request_title: str = "Making Request",
              apikey: str = ""):

    headers = {
        **headers,
        'X-Api-Key': apikey,
        "Content-Type": "application/json"
    }
    async with httpx.AsyncClient() as client:

        try:
            with console.status(request_title) as status:
                response = await client.put(url=url, params=params, headers=headers, timeout=timeout, data=data)

                return response

        except Exception as e:
            return False


async def Post(url: str,
               params: Optional[Dict] = {},
               data: Dict = {},
               headers: Optional[Dict] = {},
               timeout: int = 10,
               request_title: str = "Making Request",
               apikey: str = ""):

    headers = {
        **headers,
        'X-Api-Key': apikey,
        "Content-Type": "application/json"
    }

    async with httpx.AsyncClient() as client:

        try:
            with console.status(request_title) as status:
                response = await client.post(url=url, params=params, headers=headers, timeout=timeout, data=data)

                return response

        except Exception as e:
            return False


async def Delete(url: str,
                 params: Optional[Dict] = {},
                 headers: Optional[Dict] = {},
                 timeout: int = 10,
                 request_title: str = "Making Request",
                 apikey: str = ""):

    headers = {
        **headers,
        'X-Api-Key': apikey,
        "Content-Type": "application/json"
    }
    async with httpx.AsyncClient() as client:

        try:

            with console.status(request_title) as status:
                response = await client.delete(url=url, params=params, headers=headers, timeout=timeout)

                return response

        except Exception as e:
            return False


def creatTable(headers: List[Dict],
               data: List[Dict],
               title: str = "Table"):

    table = Table(title=title, show_header=True,
                  header_style="bold magenta", highlight=True)

    for h in headers:
        table.add_column(h['text'])

    for d in data:
        table.add_row(*d)

    return table


async def getProjects(cache: Dict, apikey: str):

    projects = cache.setdefault("projects", {})
    tasks = cache.setdefault("tasks", {})
    user = cache.get('user', {})

    tasks_request = []

    api_url = urljoin(
        BASE_API_URL,
        "workspaces/{workspace_id}/projects".format(**user)
    )

    response = await Get(url=api_url, request_title="Fetching Projects List", multiple=True, apikey=apikey)

    data = response.json()

    for i in data:
        projects[i['id']] = {
            "name": i['name'],
            "id": i['id']
        }

        api_url = urljoin(
            BASE_API_URL,
            'workspaces/{workspace_id}/projects/{projectId}/tasks'.format(
                **user,
                projectId=i['id']
            )
        )

        tasks_request.append(
            Get(url=api_url, multiple=True, apikey=apikey)
        )

    responses = await asyncio.gather(*tasks_request)

    for r in responses:
        data = r.json()

        for d in data:

            tasks[d['id']] = {
                "name": d['name'],
                "id": d['id'],
                "project_id": d['projectId'],
                "project_name": projects[d['projectId']]['name']
            }


async def showProjects(cache: Dict):
    projects = cache.get('projects', {})

    HEADERS = [
        {"text": "ID"},
        {"text": "Name"},
    ]

    DATA = []

    for p in projects:

        if len(projects[p]['name']) > 30:
            project_name = "{} ..".format(
                projects[p]['name'][:30]
            )
        else:
            project_name = projects[p]['name']

        DATA.append((
            projects[p]['id'],
            project_name
        ))

    console.print(creatTable(headers=HEADERS, data=DATA, title="Projects"))


async def showTasks(cache: Dict):
    tasks = cache.get('tasks', {})

    HEADERS = [
        {"text": "Task ID"},
        {"text": "Project Name"},
        {"text": "Name"}
    ]

    DATA = []

    for p in tasks:

        if len(tasks[p]['name']) > 30:
            task_name = "{} ..".format(
                tasks[p]['name'][:30]
            )
        else:
            task_name = tasks[p]['name']

        DATA.append((
            tasks[p]['id'],
            tasks[p]['project_name'],
            task_name
        ))

    console.print(creatTable(headers=HEADERS, data=DATA, title="Tasks"))


async def showMyTasks(cache: Dict):
    tasks = cache.get('mytask', {})

    HEADERS = [
        {"text": "Task ID"},
        {"text": "Project Name"},
        {"text": "Name"}
    ]

    DATA = []

    for p in tasks:

        if len(tasks[p]['name']) > 30:
            task_name = "{} ..".format(
                tasks[p]['name'][:30]
            )
        else:
            task_name = tasks[p]['name']

        DATA.append((
            tasks[p]['id'],
            tasks[p]['project_name'],
            task_name
        ))

    console.print(creatTable(headers=HEADERS, data=DATA, title="My Tasks"))


async def addToMyTasks(cache: Dict):

    mytask = cache.setdefault('mytask', {})
    tasks = cache.get('tasks', {})

    await showTasks(cache=cache)

    print("\n:heavy_plus_sign: Add To MyTask")

    while True:

        taskid = console.input("\nTaskid: ").strip()

        if taskid.lower() == 'q':
            return

        task = tasks.get(taskid, {})

        if not task:
            continue

        mytask[taskid] = task

        addmore = console.input("Add More? (y/n): ").strip().lower()

        if addmore == 'n':
            await wrtieCacheToDisk(cache=cache, apikey=None, init=False)
            break


async def removeMyTasks(cache: Dict):

    mytask = cache.get('mytask', {})

    if not mytask:
        return

    await showMyTasks(cache=cache)

    print("\n:x: Remove Task")

    while True:
        taskid = console.input("\nTaskid: ").strip().lower()

        if taskid == 'q':
            return

        if taskid == 'done':
            await wrtieCacheToDisk(cache=cache, apikey=None, init=False)
            break

        try:
            mytask.pop(taskid)
        except Exception as e:
            print(":x: Error failed to remove task")
            continue

        addmore = console.input("Add More? (y/n): ").strip().lower()

        if addmore == 'n':
            await wrtieCacheToDisk(cache=cache, apikey=None, init=False)
            break


async def myTaks(cache: Dict):

    mytask = cache.get('mytask', {})

    MY_TASKS_HEADERS = [
        {"text": "Option"},
        {"text": "Name"},
    ]

    MY_TASKS_OPTIONS = [
        ("1", ":memo: Show Tasks"),
        ("2", ":ledger: Show My Task"),
        ("3", ":heavy_plus_sign: Add Task"),
        ("4", ":x: Remove Task"),
        ("5", ":house: Default Task"),
        ("0", ":memo: Show My Task Menu"),
        ("Q/q", ":v: Exit Submenu")
    ]

    table = creatTable(headers=MY_TASKS_HEADERS,
                       data=MY_TASKS_OPTIONS, title="Manage My Tasks")

    print(table)

    while True:
        option = console.input("\n:id: Select Option (mytask): ")
        print()

        if option.lower() == "q":
            break

        if option == '1':
            await showTasks(cache=cache)
            continue
        if option == '2':
            await showMyTasks(cache=cache)
            continue
        if option == "3":
            await addToMyTasks(cache=cache)
            continue
        if option == "4":
            await removeMyTasks(cache=cache)
            continue
        if option == "0":
            print(table)
            continue


async def timeEntryCurrent(cache: Dict, apikey: str):

    projects: Dict = cache.get("projects", {})
    user: Dict = cache.get('user', {})
    tasks: Dict = cache.get('tasks', {})

    TABLE_HEADERS = [
        {"text": "ID"},
        {"text": "Description"},
        {"text": "Project Name"},
        {"text": "Task Name"},
        {"text": "Start"},
        {"text": "Duration"}
    ]

    TABLE_DATA = []

    api_url = urljoin(BASE_API_URL,
                      "workspaces/{workspace_id}/user/{id}/time-entries/".format(
                          **user))

    respose: httpx.Response = await Get(url=api_url, apikey=apikey)

    data = respose.json()

    for i in data:

        project_id = projects.get(i['projectId'], {})
        task_id = i['taskId']

        if task_id is not None:
            mytask = tasks.get(task_id, {})
            task_name = mytask['name'][:20]
        else:
            task_name = ""

        TABLE_DATA.append((
            i['id'],
            i['description'],
            project_id.get("name", i['projectId']),
            task_name,
            i['timeInterval']['start'],
            i['timeInterval']['duration']
        ))

    table: Table = creatTable(headers=TABLE_HEADERS,
                              data=TABLE_DATA, title="Timesheet")

    print(table)


async def createTime(cache: Dict, apikey: str):

    tasks: Dict = cache.get("tasks", {})
    mytask: Dict = cache.get("tasks", {})
    user: Dict = cache.get('user', {})

    if mytask:
        await showMyTasks(cache=cache)
    else:
        await showTasks(cache=cache)

    while True:

        current_time = datetime.now(timezone(user.get('tz')))
        end = None

        print("\n:clock1: New Time Entry")

        start = console.input(
            "Start Time (i.e 2021-07-19T12:00:00) Leave Blank to use current time: ")

        if not start:
            start = current_time
        else:
            try:
                start = datetime.strptime(
                    "{}Z".format(start), "%Y-%m-%dT%H:%M:%SZ")
            except Exception as e:
                continue

        duration = console.input(
            "Duration (Example 8h, 120m) Defaul tis 'h': ")
        taskid = console.input("Tasks ID: ")
        description = console.input("Description: ")

        if not all([duration, taskid]):
            continue

        taskid = taskid.strip()

        confirm = console.input("Add Entry? [y/n]")

        if confirm not in ['Y', 'y']:
            break

        duration = duration.strip().lower()

        if "h" in duration:
            end = start + timedelta(hours=int(duration.replace("h", "")))
        elif "m" in duration:
            end = start + timedelta(minutes=int(duration.replace("m", "")))
        else:
            end = start + timedelta(hours=int(duration))

        mytask = tasks.get(taskid, {})

        newEntry = ClokifyNewEntry(
            start=start.strftime("%Y-%m-%dT%H:%M:%SZ"),
            end=end.strftime("%Y-%m-%dT%H:%M:%SZ"),
            taskId=taskid,
            description=description,
            projectId=mytask['project_id']
        )

        api_url = urljoin(
            BASE_API_URL,
            "workspaces/{workspace_id}/time-entries".format(
                **user)
        )

        response = await Post(url=api_url, data=newEntry.json(), apikey=apikey)

        if response.status_code in [200, 201]:
            print(":+1: Entry has been addded!")
        else:
            print(":x: Failed to create entry: Response",
                  response.status_code, response.text)

        addmore = console.input("Add more? (Y/n): ")

        if addmore not in ['Y', "y"]:
            break


async def startTimer(cache: Dict, apikey: str):

    tasks: Dict = cache.get("tasks", {})
    user: Dict = cache.get('user', {})

    await showTasks(cache=cache)

    while True:

        print("\n:watch: Start A Timer")

        taskid = console.input("Tasks ID: ").strip().lower()
        description = console.input("Description: ")

        if not all([taskid]):
            continue

        if taskid == 'q' or description == 'q':
            break

        startime = datetime.utcnow()

        mytask = tasks.get(taskid, {})

        newEntry = ClokifyNewEntry(
            start=startime.strftime("%Y-%m-%dT%H:%M:%SZ"),
            end=None,
            taskId=taskid.strip(),
            description=description,
            projectId=mytask['project_id']
        )

        api_url = urljoin(
            BASE_API_URL,
            "workspaces/{workspace_id}/time-entries".format(
                **user)
        )

        response = await Post(url=api_url, data=newEntry.json(), apikey=apikey)

        if response.status_code in [200, 201]:
            print(":+1: Timer has started")
        else:
            print(":x: Failed to create entry: Response",
                  response.status_code, response.text)

        with console.status("Time") as status:
            while True:
                try:
                    now = datetime.utcnow()

                    count = str(now - startime)

                    status.update(
                        ":clock10: Timer (Ctr+C to stop timer) " + count.split(".")[0])
                    time.sleep(1)
                except KeyboardInterrupt:
                    break

        print("Time", count.split(".")[0])

        api_url = urljoin(
            BASE_API_URL,
            "workspaces/{workspace_id}/user/{id}/time-entries".format(
                **user)
        )

        response = await Path(url=api_url, request_title="Stopping Timer", apikey=apikey, data=json.dumps({"end": now.strftime("%Y-%m-%dT%H:%M:%SZ")}))

        if response.status_code in [200, 201]:
            print(":+1: Timer stopped successfully")
        else:
            print(":x: Failed to stop timer: Response",
                  response.status_code, response.text)

        addmore = console.input("Add a new timer? (y/n): ")

        if addmore.lower() == 'y':
            continue
        else:
            break


async def deleteTime(cache: Dict, apikey: str):

    user: Dict = cache.get('user', {})

    await timeEntryCurrent(cache=cache, apikey=apikey)

    while True:

        print("\nDelete Time Entry")

        entry_id = console.input("Entry ID (q to exit): ")

        if entry_id in ['Q', "q"]:
            break

        if not entry_id:
            continue

        api_url = urljoin(
            BASE_API_URL,
            "workspaces/{workspace_id}/time-entries/{time_id}".format(
                **user, time_id=entry_id.strip())
        )

        response = await Delete(url=api_url, apikey=apikey)

        if response.status_code in [200, 201, 204]:
            print(":+1: Entry Has been deleted!")
        else:
            print(":x: Failed to delete Entry: ",
                  response.status_code, response.text)

        delete_more = console.input("Delete More? (y/n): ")

        if delete_more not in ["Y", "y"]:
            break


def processUserList(user: List[Dict]):

    users = []

    for u in user:

        status = ":white_check_mark:" if u['status'] == 'ACTIVE' else ":no_entry_sign:"

        settings: Dict = u.get("settings", {})

        if not settings:
            settings = {}

        users.append((
            u['email'],
            u['name'],
            status,
            settings.get("timeZone", "N/A")
        ))

    return users


async def listUers(cache: Dict, apikey: str):

    user = cache.setdefault('user', {})

    api_url = urljoin(
        BASE_API_URL,
        "workspaces/{workspace_id}/users".format(
            **user
        )
    )

    response = await Get(url=api_url, apikey=apikey, request_title="Fetching Users")

    if response.status_code != 200:
        print(":x: Failed to get users")
        return

    TABLE_DATA = processUserList(response.json())

    TABLE_HEADERS = [
        {"text": ":e-mail: Email"},
        {"text": ":bust_in_silhouette: Name"},
        {"text": "Status"},
        {"text": ":clock10: Timezone"}
    ]

    table = creatTable(headers=TABLE_HEADERS, data=TABLE_DATA, title="Users")

    print(table)


async def userInfo(cache: Dict, apikey: str):

    user = cache.setdefault('user', {})

    api_url = urljoin(
        BASE_API_URL,
        "user"
    )

    res = await Get(url=api_url, request_title="Fetching User Info", multiple=True, apikey=apikey)

    if res.status_code != 200:
        print("\nInvalid API Key", res.text)
        sys.exit()

    data = res.json()

    user['id'] = data['id']
    user['email'] = data['email']
    user['name'] = data['name']
    user['workspace_id'] = data['activeWorkspace']
    user['tz'] = data['settings']['timeZone']


async def wrtieCacheToDisk(cache: Dict, apikey: str, init: bool = True):

    if init is True:
        await userInfo(cache=cache, apikey=apikey)
        await getProjects(cache=cache, apikey=apikey)

    with open(os.path.join(CONFIG_DIR, 'cache.json'), 'w') as f:
        f.write(json.dumps(cache))


async def loadCacheFromDisk(cache: Dict):

    with open(os.path.join(CONFIG_DIR, 'cache.json')) as f:

        cache.update(json.loads(f.read()))


async def getCacheFromDisk(cache: Dict, apikey: str):

    with console.status("Loading cache from disk") as status:

        status.update("Checking for cache file ")
        await asyncio.sleep(.1)

        if not os.path.exists(os.path.join(CONFIG_DIR, 'cache.json')):

            status.update(
                "Cache File is Missing, Fetching UserInfo, Projects and writing to disk")

            await wrtieCacheToDisk(cache=cache, apikey=apikey)

            return

        # Load cache file
        status.update("Loading cache from disk")
        await loadCacheFromDisk(cache=cache)


async def loadAPIKey():

    if not os.path.exists(CONFIG_DIR):
        os.mkdir(CONFIG_DIR)

    API_KEY_LOCATION = os.path.join(CONFIG_DIR, 'key')

    if not os.path.exists(API_KEY_LOCATION):

        while True:
            api_key = console.input("API KEY (q To Quit): ")

            api_key = api_key.strip()

            if api_key == 'q':
                sys.exit()

            with open(API_KEY_LOCATION, 'w') as f:
                f.write(api_key)

            return api_key

    with open(API_KEY_LOCATION) as f:

        return f.read()


async def menu(cache: Dict, apikey: str):

    user = cache.get('user', {})

    HEADERS = [
        {"text": "Option"},
        {"text": "Description"},
    ]

    DATA = [
        ("1", ":house: List Tasks"),
        ("2", ":ledger: Show Time Entries"),
        ("3", ":watch: Add Time"),
        ("4", ":skull: Delete Time"),
        ("5", ":clock1: Start Timer"),
        ("6", ":clipboard: List Projects"),
        ("7", ":busts_in_silhouette: List Users"),
        ("8", ":house: Manage My Tasks"),
        ("0", ":memo: Show Menu"),
        ("00", ":floppy_disk: Update Cache File"),
        ("clear", ":computer: Clear Screen"),
        ("Q/q", ":v: Quit")
    ]

    table = creatTable(data=DATA, headers=HEADERS,
                       title=":clock9: ClockiPy Menu :clock10:")

    print("\n:wave::wave: Welcome! :bust_in_silhouette: {}\n".format(
        user.get('name', 'N/A')))

    console.print(table)

    while True:
        action = console.input("\n:id: Select Menu Option: ")
        print()

        if action == 'q' or action == 'Q':
            break
        elif action == '1':
            await showTasks(cache=cache)
            continue
        elif action == '2':
            await timeEntryCurrent(cache=cache, apikey=apikey)
            continue
        elif action == '3':
            await createTime(cache=cache, apikey=apikey)
            continue
        elif action == '4':
            await deleteTime(cache=cache, apikey=apikey)
            continue
        elif action == '5':
            await startTimer(cache=cache, apikey=apikey)
            continue
        elif action == '6':
            await showProjects(cache=cache)
            continue
        elif action == '7':
            await listUers(cache=cache, apikey=apikey)
            continue
        elif action == '8':
            await myTaks(cache=cache)
            continue
        elif action == 'clear':
            system('clear')
            continue
        elif action == '0':
            print(table)
            continue
        elif action == '00':
            await wrtieCacheToDisk(cache=cache, apikey=apikey)
            continue


async def main(cache: Dict):
    api_key = await loadAPIKey()
    await getCacheFromDisk(cache=cache, apikey=api_key)
    await menu(cache=cache, apikey=api_key)


def entry():
    global CACHE
    asyncio.run(main(cache=CACHE))


if __name__ == '__main__':

    asyncio.run(main(cache=CACHE))
