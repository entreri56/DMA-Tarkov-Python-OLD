import memprocfs
import struct
import time
import pygame

# Define class Offsets with memory offsets
class Offsets:
    GOM = 0x17FFD28
    LocalGameWorld = (0x30, 0x18, 0x28)
    GameObject = ObjectName = 0x60
    MainPlayer = 0x148
    RegisteredPlayers = 0xF0 #uint64_t
    

print("Initializing memory reader...")
vmm = memprocfs.Vmm(['-device', 'fpga'])
procd = vmm.process('EscapeFromTarkov.exe')
module_client = procd.module('UnityPlayer.dll')
mode = module_client.base
print("Memory reader initialized.")


# Define class BaseObject to represent base game objects
class BaseObject:
    def __init__(self, base_object: bytes):
        self.previousObjectLink, self.nextObjectLink, self.obj = struct.unpack("QQQ", base_object)

# Define class GameObjectManager to represent game object management
class GameObjectManager:
    def __init__(self, gom: bytes):
        # Unpack the bytes into different attributes representing different lists of game objects
        self.LastTaggedNode, self.TaggedNodes, self.LastMainCameraTaggedNode, self.MainCameraTaggedNodes, self.LastActiveNode, self.ActiveNodes = struct.unpack("QQQQQQ", gom)

# Define functions to read memory
def read_ptr(process, address: int):
    return int.from_bytes(process.memory.read(address, 8), 'little')

def read_str(process, address: int, max_length: int):
    try:
        decoded_str = process.memory.read(address, max_length).decode('utf-8', errors='replace').split('\0', 1)[0]
        return decoded_str
    except UnicodeDecodeError:
        print("Error: Invalid UTF-8 encoding for address:", hex(address))
        bytes_read = process.memory.read(address, max_length)
        print("Bytes read:", bytes_read)
        return "Error: Invalid UTF-8 encoding"

def read_value(process, address: int, size: int):
    return process.memory.read(address, size, memprocfs.FLAG_NOCACHE)

def read_int_memory(process, address):
    try:
        return struct.unpack("<I", process.memory.read(address, 4))[0]
    except struct.error as e:
        print("Error reading integer memory at address:", hex(address), e)
        return None


def read_float_memory(process, address):
    # Read 4 bytes of memory and check if the read was successful
    try:
        memory = process.memory.read(address, 4)
    except memprocfs.errors.ReadError:
        print("Error reading memory at address:", hex(address))
        return None

    # Check if we have successfully read 4 bytes
    if len(memory) == 4:
        # Unpack the memory into a float value
        return struct.unpack("<f", memory)[0]
    else:
        print("Error: Could not read 4 bytes of memory at address:", hex(address))
        return None


def GetObjectFromList(process, activeObjectsPtr: int, lastObjectPtr: int, objectName: str):
    activeObject = BaseObject(
        read_value(process, activeObjectsPtr, struct.calcsize("LLL" * 2)))
    try:
        lastObject = BaseObject(read_value(process, lastObjectPtr, struct.calcsize("LLL" * 2)))
    except struct.error:
        print("Error reading game list object.")
        return None

    if activeObject.obj != 0x0:
        while activeObject.obj != 0x0:
            objectNamePtr = read_ptr(process, activeObject.obj + Offsets.GameObject)
            objectNameStr = read_str(process, objectNamePtr, 64)

            if objectName.lower() in objectNameStr.lower():
                print(f"Found {objectNameStr}; Base: {hex(activeObject.obj + Offsets.GameObject)}")
                return activeObject.obj

            if activeObject.obj == lastObject.obj:
                break

            try:
                activeObject = BaseObject(
                    read_value(process, activeObject.nextObjectLink, struct.calcsize("LLL" * 2)))
            except struct.error:
                print("Error reading game list object.")
                return None

    print(f"Could not find {objectName}")

# Initialize Pygame
pygame.init()
width, height = 1000, 1000
screen = pygame.display.set_mode((width, height))

def Main():
    # Find GameWorld address
    gom_address = read_ptr(procd, mode + Offsets.GOM)
    gom_data = read_value(procd, gom_address, struct.calcsize("LLLLLL" * 2))
    gom = GameObjectManager(gom_data)

    activeNodes = read_ptr(procd, gom.ActiveNodes)
    lastActiveNode = read_ptr(procd, gom.LastActiveNode)
    while True:
        gameWorld = GetObjectFromList(procd, activeNodes, lastActiveNode, "GameWorld")
        if gameWorld is not None:
            break
        # Retries if GameWorld not found
        activeNodes = read_ptr(procd, gom.ActiveNodes)
        lastActiveNode = read_ptr(procd, gom.LastActiveNode)
        time.sleep(1)

    # Once GameWorld found, get LocalGameWorld pointer
    lgw_ptr = read_ptr(procd, gameWorld + Offsets.LocalGameWorld[0])
    lgw_ptr = read_ptr(procd, lgw_ptr + Offsets.LocalGameWorld[1])
    lgw_ptr = read_ptr(procd, lgw_ptr + Offsets.LocalGameWorld[2])

    print("GameWorld address:", hex(gameWorld))
    print("LocalGameWorld address:", hex(lgw_ptr))




    return lgw_ptr






def read_pointer(procd, address):
    try:
        # Read 8 bytes from memory
        pointer_bytes = procd.memory.read(address, 8)
        # Unpack the bytes as a little-endian unsigned long long integer
        entity_ptr = struct.unpack("<Q", pointer_bytes)[0]
        return entity_ptr
    except Exception as e:
        print("Error reading pointer from memory:", e)
        return None





def MemoryRead(lgw_ptr):

    MainPlayerPtr = read_ptr(procd, lgw_ptr + Offsets.MainPlayer)
    print("MainPlayer address:", hex(MainPlayerPtr))


    RegisteredPtr = read_ptr(procd, lgw_ptr + Offsets.RegisteredPlayers)
    print("RegisteredPlayers address:", hex(RegisteredPtr))
    running = True


    MainPlayerPtrAddress= read_ptr(procd, MainPlayerPtr + 0x28)
    print("MainPlayerPtrAddress address:", hex(MainPlayerPtrAddress))


    MainPlayerAddressX = MainPlayerPtrAddress + 0xC0
    MainPlayerAddressY = MainPlayerPtrAddress + 0xC8
    print("MainPlayerAddressX address:", hex(MainPlayerAddressX))
    print("MainPlayerAddressY address:", hex(MainPlayerAddressY))


    
    # Read the pointer at the offset 0x10 from RegisteredPlayers address
    players_list_ptr_read = read_ptr(procd, RegisteredPtr + 0x10)
    print("PlayerList address:", hex(players_list_ptr_read ))

    while running:

        entities = []

        # Iterate through the player list
        for i in range(40):

            scatter_memory = procd.memory.scatter_initialize()
            scatter_memory.prepare(MainPlayerAddressX, 4)
            scatter_memory.execute()
            PlayerXValue = scatter_memory.read_type(MainPlayerAddressX, 'f32')
            scatter_memory.close()

            print(f"Player X value: ",  PlayerXValue)

            scatter_memory = procd.memory.scatter_initialize()
            scatter_memory.prepare(MainPlayerAddressY, 4)
            scatter_memory.execute()
            PlayerYValue = scatter_memory.read_type(MainPlayerAddressY, 'f32')
            scatter_memory.close()

            print(f"Player Y value: ",  PlayerYValue)

            PlayerScreenX = int(PlayerXValue + width / 2)
            PlayerScreenY = int(PlayerYValue + height / 2)

            
            # Read the pointer at the current offset
            entity_addressptr = players_list_ptr_read + i * 0x8
            print("Entity Address:", hex(entity_addressptr))
            
            if entity_addressptr == 0:
                continue

            entityptr = read_ptr(procd, entity_addressptr)
            entityX = entityptr + 0x738
            entityY = entityptr + 0x740
            print("EntityX Address:", hex(entityX))
            print("EntityY Address:", hex(entityY))


            scatter_memory = procd.memory.scatter_initialize()
            scatter_memory.prepare(entityX, 4)
            scatter_memory.execute()
            EntityXValue = scatter_memory.read_type(entityX, 'f32')
            scatter_memory.close()


            scatter_memory = procd.memory.scatter_initialize()
            scatter_memory.prepare(entityY, 4)
            scatter_memory.execute()
            EntityYValue = scatter_memory.read_type(entityY, 'f32')
            scatter_memory.close()


            if isinstance(EntityXValue, float) and isinstance(EntityYValue, float):
                # Append valid entities to the list
                entities.append((EntityXValue, EntityYValue))
                print(f"Entity {i}: X value = {EntityXValue}, Y value = {EntityYValue}")

        # Clear the screen
        screen.fill((0, 0, 0))

        # Draw entities on the Pygame screen
        for x, y in entities:
            # Check if x and y are numbers
            if isinstance(x, (int, float)) and isinstance(y, (int, float)):
                # Shift the origin to the center of the window
                screen_x = int(x + width / 2)
                screen_y = int(y + height / 2)

                # Draw entities
                pygame.draw.circle(screen, (255, 0, 0), (screen_x, screen_y), 3)
                pygame.draw.circle(screen, (0, 255, 0), (PlayerScreenX, PlayerScreenY), 5)
            else:
                print(f"Invalid coordinates for entity: ({x}, {y})")


        pygame.display.update()

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False



# Main function
def main():
    lgw_ptr = Main()  
    MemoryRead(lgw_ptr)




# Run the main function
if __name__ == "__main__":
    main()
