import ctypes
import base64
from ctypes import wintypes

# Load crypt32.dll for DPAPI functions
crypt32 = ctypes.windll.crypt32


# Constants for DPAPI
CRYPTPROTECT_LOCAL_MACHINE = 0x04  # Ties encryption to machine (you can remove this if you want user context)
CRYPTPROTECT_UI_PROMPT = 0x00  # Enables UI prompt for user authentication (Windows Hello)


# Structures for DPAPI calls
class DataBlob(ctypes.Structure):
    _fields_ = [("cbData", wintypes.DWORD),
                ("pbData", ctypes.POINTER(ctypes.c_byte))]


def encrypt_data(data):
    data_blob_in = DataBlob(len(data), ctypes.cast(ctypes.create_string_buffer(data.encode('utf-8')), ctypes.POINTER(ctypes.c_byte)))
    data_blob_out = DataBlob()

    # Use CRYPTPROTECT_UI_PROMPT to allow Windows Hello authentication prompt
    if crypt32.CryptProtectData(ctypes.byref(data_blob_in), None, None, None, None, CRYPTPROTECT_UI_PROMPT, ctypes.byref(data_blob_out)):
        encrypted_data = ctypes.string_at(data_blob_out.pbData, data_blob_out.cbData)
        return base64.b64encode(encrypted_data).decode('utf-8')
    else:
        raise ctypes.WinError()


def decrypt_data(encrypted_data):
    data_blob_in = DataBlob(len(encrypted_data), ctypes.cast(ctypes.create_string_buffer(base64.b64decode(encrypted_data)), ctypes.POINTER(ctypes.c_byte)))
    data_blob_out = DataBlob()

    # Use CRYPTPROTECT_UI_PROMPT to trigger Windows Hello authentication prompt
    if crypt32.CryptUnprotectData(ctypes.byref(data_blob_in), None, None, None, None, CRYPTPROTECT_UI_PROMPT, ctypes.byref(data_blob_out)):
        return ctypes.string_at(data_blob_out.pbData, data_blob_out.cbData).decode('utf-8')
    else:
        raise ctypes.WinError()
