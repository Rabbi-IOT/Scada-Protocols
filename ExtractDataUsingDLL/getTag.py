import ctypes
import time
import datetime

serverName = None
userName = b"ATI"
password = b"Ati@123"
flags = 0

kernel32 = ctypes.WinDLL('kernel32')
get_last_error = kernel32.GetLastError
get_last_error.restype = ctypes.c_ulong

def loadDLL():    
    try:
        ctAPI = ctypes.WinDLL(r'C:\Program Files (x86)\Schneider Electric\Citect SCADA 2018\Bin\Bin (x64)\CtApi.dll')
        if ctAPI:
            print(datetime.datetime.now(),"DLL loaded successfully")
            return ctAPI
        else:
            print(datetime.datetime.now(),"Error loading DLL")   
    except Exception as e:
        print(datetime.datetime.now(),e)

ctapi = loadDLL()

# Define necessary types
DWORD = ctypes.c_ulong
HANDLE = ctypes.c_void_p
LPCTSTR = ctypes.c_char_p
LPSTR = ctypes.c_char_p

dwType = 0x130

# Define Citect API function prototypes
ctapi.ctTagRead.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_ulong]
ctapi.ctTagRead.restype = ctypes.c_bool

ctapi.ctOpen.argtypes = [LPCTSTR, LPCTSTR, LPCTSTR, DWORD]
ctapi.ctOpen.restype = HANDLE


ctapi.ctFindFirst.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.POINTER(ctypes.c_void_p), ctypes.c_ulong]
ctapi.ctFindFirst.restype = ctypes.c_void_p 

ctapi.ctGetProperty.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_void_p, ctypes.c_ulong, ctypes.POINTER(ctypes.c_ulong), ctypes.c_ulong]
ctapi.ctGetProperty.restype = ctypes.c_bool


ctapi.ctFindNext.argtypes = [HANDLE, ctypes.POINTER(HANDLE)]
ctapi.ctFindNext.restype = ctypes.c_int

ctapi.ctFindClose.argtypes = [HANDLE]

def get_all_tag_names(server, username, password) -> list:
    # Open connection to Citect SCADA server
    hCTAPI = ctapi.ctOpen(server, username, password, 0)
    print(datetime.datetime.now(),"Connection Status:",hCTAPI)
    bufferSize = 256
    tagValueBuffer = ctypes.create_string_buffer(bufferSize)
    temp =ctapi.ctTagRead(hCTAPI,b"Archive1_T", tagValueBuffer, bufferSize)
    print("Temp:",tagValueBuffer.value.decode().strip('\x00'))
    if not hCTAPI:
        print("No Tags Found::hCTAPI")
        return []

    try:
        # Find the first tag in the "Tag" table
        hFind = HANDLE()
        objectFound = ctapi.ctFindFirst(hCTAPI, b"LocalTag", b"*", ctypes.byref(hFind), 0) 
        print(datetime.datetime.now(),"ctFindFirst:",objectFound)
        if objectFound is None:
            return []  # Return empty list if no tags found
        tag_names = []
        tag_name_buffer = ctypes.create_string_buffer(4096)

        # Iterate through all tags and retrieve their names
        while True:
            propertyFound = ctapi.ctGetProperty(hFind, b"Name", tag_name_buffer, ctypes.sizeof(tag_name_buffer), None, dwType)
            print(datetime.datetime.now(),"ctGetProperty:",propertyFound)
            if propertyFound:
                tag_name = tag_name_buffer.value.decode()
                print(tag_name)
                if tag_name:
                   tag_names.append(tag_name)
            else:
                error_code = get_last_error()
                print(f"ctGetProperty failed with error code: {error_code}")        
            if not ctapi.ctFindNext(hFind, ctypes.byref(hFind)):
                break
    except Exception as e:
        print(datetime.datetime.now(),e)


# Call the function to get all tag names
all_tag_names = get_all_tag_names(serverName, userName, password)

# Print all tag names
print("all_tag_names",all_tag_names)
