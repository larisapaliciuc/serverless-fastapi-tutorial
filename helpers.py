def write_log(message=""):
    with open("log.txt", mode="a") as log_file:
        content = f"notification: {message}"
        log_file.write(content)