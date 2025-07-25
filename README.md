Make a team of Claude Code working together for you, completely hands-off.

First install *Expect*:

```bash
sudo apt install expect
```

Make sure you have Claude Code installed.

Modify the task.md to describe the task.

Then open multiple terminals, run the following scripts one by one.

```bash
# In the first terminal
expect supervisor.exp
```

```bash
# In the second terminal
expect worker.exp
```

```bash
# In the third terminal
expect tester.exp
```

...

You can edit the agents' prompts by editing the .exp files.

Edit the round limit at

```
# worker.exp
for {set i 2} {$i <= {round_limit} {incr i} {
```

After task finished, you can run

```bash
python chat_to_html.py
```

to visualize the chat history.
