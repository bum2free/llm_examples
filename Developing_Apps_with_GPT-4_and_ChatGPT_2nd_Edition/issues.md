# TypeError: Client.__init__() got an unexpected keyword argument 'proxies'
The original book uses openai==1.14.1, which gets the following errors.
Mightbe due to http_proxy environment is set.

Upgrade to use openal==1.106.0(latest version by now) could resolve the problem.
```
$ python3 Chap2_02_ChatCompletion/run.py
Traceback (most recent call last):
  File "/home/eric/Data-1/work-llm/llm_examples/Developing_Apps_with_GPT-4_and_ChatGPT_2nd_Edition/Chap2_02_ChatCompletion/run.py", line 6, in <module>
    client = OpenAI()
  File "/home/eric/Data-1/work-llm/llm_examples/Developing_Apps_with_GPT-4_and_ChatGPT_2nd_Edition/.venv/lib/python3.10/site-packages/openai/_client.py", line 112, in __init__
    super().__init__(
  File "/home/eric/Data-1/work-llm/llm_examples/Developing_Apps_with_GPT-4_and_ChatGPT_2nd_Edition/.venv/lib/python3.10/site-packages/openai/_base_client.py", line 801, in __init__
    self._client = http_client or SyncHttpxClientWrapper(
TypeError: Client.__init__() got an unexpected keyword argument 'proxies'
```
