import os
import json
import openai
from dotenv import load_dotenv


# Setup the OpenAI client to use either Azure, OpenAI or Ollama API
load_dotenv("/media/uberdev/ddrv/gitFolders/python_de_learners_data/.env")
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# print(os.getenv("OPENAI_API_KEY"))


def list_directory_contents_json(path):
    """Get the files present in the dir path, and use that to answer questions on them"""
    # Assume the data provided is part of your context and use it to answer the
    # questions on the files in the directory
    contents = []

    for entry in os.scandir(path):
        info = entry.stat()
        details = {
            "name": entry.name,
            "is_directory": entry.is_dir(),
            "size": info.st_size,
            "permissions": oct(info.st_mode),
            "last_accessed": info.st_atime,
            "last_modified": info.st_mtime,
            "created": info.st_ctime,
        }
        contents.append(details)

    return json.dumps(contents, indent=4)


def read_file_contents(path: str):
    """Read the contents and return the lines, word counts and file content of the file in given path"""
    try:
        with open(path, "r") as file:
            data = file.read()
            return json.dumps({
                "lines_count": len(data.splitlines()),
                "words_count": len(data.split(" ")),
                "data": data,
            })
    except FileNotFoundError:
        return f"File not found: {path}"
    except Exception as e:
        return f"An error occurred: {str(e)}"


def update_file_contents(path: str, data: str):
    """Update the file in given path with the data return status of the update"""
    try:
        with open(path, "a") as file:  # 'a' mode appends to the file
            file.write(data)
            return "File updated successfully."
    except Exception as e:
        return f"An error occurred: {str(e)}"


def create_file_contents(path: str, data: str = "PlaceHolder"):
    """Create the file at the given path, along with the provided data"""
    try:
        with open(
            path, "w"
        ) as file:  # 'w' mode creates a new file, erases earlier content
            file.write(data)
            return "File created with data successfully."
    except Exception as e:
        return f"An error occurred: {str(e)}"


def delete_file(path: str):
    """Delete the file at the given path, and return the status"""
    try:
        if os.path.exists(path):
            os.remove(path)
            return f"File deleted successfully: {path}"
        else:
            return f"File not found: {path}"
    except Exception as e:
        return f"An error occurred: {str(e)}"


def run_conversation(user_request: str):
    # Step 1: send the conversation and available functions to the model
    messages = [
        {
            "role": "system",
            "content": """
                You are a helpful assistant designed to manipulate the filesystem.
                Only use the functions you have been provided with.
                Adhere to the descriptions for the functions/tools provided.

                # Tools available:
                - list_directory_contents_json, 
                    Returns a json array, with the list of files and folders in the current path. 
                - read_file_contents,
                    Returns the json of words and lines count along with the file content
                - delete_file:
                    Delete the file at the given path, and return the status
                - create_file_contents:
                    Create the file at the given path, along with the provided data
                - update_file_contents
                    Update the file in given path with the data return status of the update
            """,
        },
        # we are hard coding a path for this discussion /home/uberdev/
        {
            "role": "user",
            # "content": "Provide the list of files at the /home/uberdev path. Count the number of directories and files including hidden info",
            "content": user_request,
        },
    ]

    tools = [
        {
            "type": "function",
            "function": {
                "name": "list_directory_contents_json",
                "description": "Lists the files and folders in the given path.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "path": {
                            "type": "string",
                            "description": "The path of the operating file system",
                        },
                    },
                    "required": ["path"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "create_file_contents",
                "description": "Creates the file at given path with the data.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "path": {
                            "type": "string",
                            "description": "The path of the operating file system",
                        },
                        "data": {
                            "type": "string",
                            "description": "The data to place inside the created file. Its optional",
                        },
                    },
                    "required": ["path"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "read_file_contents",
                "description": "Reads the file at given path returns the content details along with data.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "path": {
                            "type": "string",
                            "description": "The path of the operating file system",
                        },
                    },
                    "required": ["path"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "update_file_contents",
                "description": "Updates the file at given path with the data provided to it.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "path": {
                            "type": "string",
                            "description": "The path of the operating file system",
                        },
                        "data": {
                            "type": "string",
                            "description": "The data to place inside the file to be updated",
                        },
                    },
                    "required": ["path", "data"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "delete_file",
                "description": "Deletes the file at given path returns the status.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "path": {
                            "type": "string",
                            "description": "The path of the operating file system",
                        },
                    },
                    "required": ["path"],
                },
            },
        },
    ]

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        response_format={"type": "json_object"},
        messages=messages,
        tools=tools,
        tool_choice="auto",  # auto is default, but we'll be explicit
        temperature=0,  # Adjust the variance by changing the temperature value (default is 0.8)
    )
    print("Completed first request\n")

    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls

    print("The tools to call returned by LLM: \n")
    print(tool_calls)

    # Step 2: check if the model wanted to call a function
    print("Enumerating the tool calls\n")
    if tool_calls:
        messages.append(response_message)  # extend conversation with assistant's reply
        available_functions = {
            "list_directory_contents_json": list_directory_contents_json,
            "read_file_contents": read_file_contents,
            "create_file_contents": create_file_contents,
            "update_file_contents": update_file_contents,
            "delete_file": delete_file,
        }

        for tool_call in tool_calls:
            # Note: the JSON response may not always be valid; be sure to handle errors
            function_name = tool_call.function.name
            if function_name not in available_functions:
                return "Function " + function_name + " does not exist"
            print(
                f"Function args identified by llm: {tool_call.function.arguments} for function : {function_name}\n"
            )
            # Step 3: call the function with arguments if any
            function_to_call = available_functions[function_name]
            function_args = json.loads(tool_call.function.arguments)
            function_response = function_to_call(**function_args)

            # Step 4: send the info for each function call and function response to the model
            print(
                "function return is appended to message, and 2nd request is made ready"
            )
            messages.append({
                "tool_call_id": tool_call.id,
                "role": "tool",
                "name": function_name,
                "content": function_response,
            })  # extend conversation with function response

        second_response = client.chat.completions.create(
            model="gpt-4o-mini",
            response_format={"type": "json_object"},
            messages=messages,
        )  # get a new response from the model where it can see the function response
        return second_response


# print(read_file_contents("/home/uberdev/history.txt"))
# print(update_file_contents("/home/uberdev/history.txt", "added by function"))
# print(create_file_contents("/home/uberdev/funcreate.txt", "added by function"))
# print(delete_file("/home/uberdev/funcreate.txt"))

if __name__ == "__main__":
    print("""This bot can operate on your file.
    - Can return a json array, with the list 
    of files and folders in the current path. 
    - Reads a file & returns the json of words
    and lines count along with the file content
    - Delete the file at the given path, 
    and return the status
    - Create the file at the given path, 
    along with the provided data
    - Update the file in given path with the
    data return status of the update
    You must provide the data you want to 
    'append' to the file.

    Well lets begin... 
        """)

    while True:
        user_post = input("Start your Convo : ")

        result = run_conversation(user_request=user_post)

        message_content = result.choices[0].message.content

        print("The final message is:\n")

        print(message_content)

        print("Ctrl + D to exit")
