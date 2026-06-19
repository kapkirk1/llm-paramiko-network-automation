import paramiko,json,ollama,time

def chat_bot(user_input):
    response=ollama.chat(model='llama3.2:1b',messages=[
                {
                    'role': 'system',
                    'content': '''
    You are a network automation assistant.

    Your task is to convert the user's request into network CLI commands and identify the target device.

    Return ONLY valid JSON.

    Rules:

    * Do not include explanations.
    * Do not include markdown.
    * Do not include code fences.
    * Always return a JSON object.
    * Always return the device name.
    * Always return commands as a list called "commands".
    * If only one command is required, return a list containing a single command.
    * Use short device names such as r1, r2, r3, etc.

    Example 1:

    {
    "devices": ["r2"],
    "commands": [
    "show ip interface brief"
    ]
    }

    Example 2:

    User: Show interface status and routing table on r1

    {
    "devices": ["r1"],
    "commands": [
    "show ip interface brief",
    "show ip route"
    ]
    }

    Example 3:

    User: Show interface status and routing table on r1 and r2

    {
    "devices": ["r1","r2"]
    "commands": [
    "show ip interface brief",
    "show ip route"
    ]
    }

    Return ONLY valid JSON.


        '''
                },
                {
                    'role': 'user',
                    'content': user_input
                }
            ]
        )
    try:
        response_json=json.loads(response['message']['content'])
        print(response_json)
        return response_json
    except Exception as e:
        print("JSON Parsing failed",e)

def connection(inventory,response_json):
    conn=paramiko.SSHClient()
    conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    for device in response_json['devices']:
        if not (inventory.get(device)):
            print("Unknown device",device)
        else:
            print("Connecting to ",device)
            try:
                conn.connect(**inventory.get(device))
                shell=conn.invoke_shell()
                for command in response_json['commands']:
                    shell.send(f'{command}\n')
                    time.sleep(2)
                    print(shell.recv(1000).decode())
                conn.close()
                print("Closing the connection to",device)
            except Exception as e:
                print("Failed to connect ",device,e)

inventory={
    'r1': {
        'hostname':'192.168.56.116',
        'username':'cisco',
        'password':'cisco',
        'look_for_keys':False },
'r2':{
    'hostname':'192.168.56.115',
    'username':'admin',
    'password':'admin',
    'look_for_keys':False
}
}


user_input=input("Question? ")
response_json=chat_bot(user_input)
if(response_json):
    connection(inventory,response_json)