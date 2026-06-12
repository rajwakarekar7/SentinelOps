import json

def load_memory():

    try:

        file= open("memory.json", "r")

        memory = json.load(file)

        file.close()

        return memory
    
    except:

        return {}
    
def save_memory(memory):

    print("Saving memory...")

    file = open("memory.json", "w")

    json.dump(memory , file , indent=4)

    file.close()

    print("Memory saved successfully")