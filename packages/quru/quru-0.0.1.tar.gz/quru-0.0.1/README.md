# Quru in one sentence
Quru is a python workflow framework to easily swarm up a bunch of workers to streamly process tasks.

# What "Quru" means?
Quru (Chinese 瞿如, pronounce keeru) is a bird-like beast with human face and three feet, initially described in Shan Hai Jing, a classic book that describes mythic geography and beasts. 

![Quru](quru.png "Quru")


# How to run demo
You will need to setup a rabbitmq and redis instances to get Quru running. A docker compose file for quick setup is provided in `demo` folder.
1. In your terminal, `cd` to the demo folder.
2. Run `make run-infra` to get rabbitmq and redis running.
3. Run `python worker.py`. This instance starts the worker that handles tasks.
4. Run `python sender.py`. This instance periodically dispatches tasks to worker.
