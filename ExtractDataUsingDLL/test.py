import ctypes

try:
    ctAPI = ctypes.WinDLL(r'c:\Users\scada\Desktop\ExtractDataUsingDLL\CtApi.dll')
    print("DLL loaded successfully")
except Exception as e:
    print("Error loading DLL:", e)

# Define argument types and return type for ctOpen function
ctAPI.ctOpen.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_ulong]
ctAPI.ctOpen.restype = ctypes.c_void_p 

flags = 0  # You can adjust this according to your requirements

try:
    connectionHandle = ctAPI.ctOpen(None, None, None, flags)
    print("connectionHandle:",connectionHandle)
    if connectionHandle:
        print("Connected to Server")
    else:
        print("Failed to open connection")
        error_code = ctypes.windll.kernel32.GetLastError()
        print("Error code:", error_code)
except Exception as e:
    print("Error:", e)
