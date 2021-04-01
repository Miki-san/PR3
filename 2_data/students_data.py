import requests
import matplotlib.pyplot as plt
import time

main_url = "https://raw.githubusercontent.com/true-grue/kispython/main/pract3/"

messages = requests.get(main_url + "messages.json").json()
failed = requests.get(main_url + "failed.json").json()
table = requests.get(main_url + "table.json").json()

msg_format = "%a, %d %b %Y %H:%M:%S %z"
messages = {(m["subj"].upper(), time.strptime(
    m["date"].split(" (")[0], msg_format)) for m in messages}

table = table["data"]

fig, axs = plt.subplots(2, 2, figsize=(12, 12))
fig2, axs2 = plt.subplots(2, 1, figsize=(20, 10))


def parse_error(error_dict, err):
    for e in err:
        done = False
        for m in error_dict:
            if m in str(e):
                done = True
                error_dict[m] += 1
        if not done:
            error_dict["wrong answer"] += 1


daily_activity = {i: 0 for i in range(24)}

for m in messages:
    daily_activity[m[1].tm_hour] += 1
axs[0][0].grid(zorder=-1)
axs[0][0].bar(range(24), daily_activity.values(), zorder=3)
axs[0][0].set_xlabel('Hours')
axs[0][0].set_title('Daily activity')

week_activity = {i: 0 for i in range(7)}

for m in messages:
    week_activity[m[1].tm_wday] += 1
axs[0][1].grid(zorder=-1)
axs[0][1].bar(range(7), week_activity.values(), zorder=3)
axs[0][1].set_xlabel('Days')
axs[0][1].set_title('Week activity')

group_activity = {}
for m in messages:
    k = m[0].split(" ")[0]
    group_activity[k] = 0
for m in messages:
    k = m[0].split(" ")[0]
    group_activity[k] += 1
axs2[0].grid(zorder=-1)
axs2[0].bar(group_activity.keys(), group_activity.values(), zorder=3)
axs2[0].set_xlabel('Groups')
axs2[0].set_title('Group activity')

correct = {}
for i in table:
    correct[i[0]] = 0
for i in table:
    correct[i[0]] += int(i[3])
axs2[1].grid(zorder=-1)
axs2[1].bar(correct.keys(), correct.values(), zorder=3)
axs2[1].set_xlabel('Groups')
axs2[1].set_title('Correct answers')

tasks = {}
for i in table:
    tasks[i[2]] = 0
for i in table:
    tasks[i[2]] += int(i[3])
axs[1][0].grid(zorder=-1)
axs[1][0].bar(tasks.keys(), tasks.values(), zorder=3)
axs[1][0].set_xlabel('Tasks')
axs[1][0].set_title('Correct answers')

errors = {"list index out of range": 0,
          "is not defined": 0,
          "unsupported operand type": 0,
          "positional arguments": 0,
          "no attribute": 0,
          "wrong answer": 0,
          "referenced before assignment": 0,
          "None": 0,
          "could not convert": 0}

for i in failed.values():
    parse_error(errors, i)
axs[1][1].pie(errors.values())
axs[1][1].legend(loc='center left', labels=errors.keys(), prop={'size': 6})

plt.show()
