# Parser/reformatter for WAD files
# Based on https://doomwiki.org/wiki/WAD#Flats.2C_Sprites.2C_and_Patches

import sys
import os

wad_file = None
dump_file = None
wad_name = ""
if len(sys.argv) > 1:
    try:
        wad_name = sys.argv[1]
        wad_file = open(sys.argv[1], "rb")
    except FileNotFoundError:
        print("Can't find file.")
        exit()
    except PermissionError:
        print("Permission denied.")
        exit()
    except Exception as e:
        print("Unexpected error occured: " + e)
        exit()
else:
    try:
        wad_name = input("Wad file name: ")
        wad_file = open(wad_name, "rb")
    except FileNotFoundError:
        print("Can't find file.")
        exit()
    except PermissionError:
        print("Permission denied.")
        exit()
    except Exception as e:
        print("Unexpected error occured: " + e)
        exit()

try:
    dump_file = open("dump.txt","x")
except Exception as e:
    print("Log file already exists.")

dump_file = open("dump.txt","a")
print("Appending dump to file")


def log(str):
    print(str)
    dump_file.write(str + "\n")

if not wad_file:
    exit()

# Parse header
log("### Dump of " + wad_name + " ###")
# 4 byte ASCII identifier
head_id = " " * 4
# Number of lumps in file
head_numlumps = int
# Pointer to the beginning of the directory
head_infotableofs = int

head_id = wad_file.read(4).decode('ascii')
head_numlumps = int.from_bytes(wad_file.read(4), byteorder='little')
head_infotableofs = int.from_bytes(wad_file.read(4), byteorder='little')
log("HEAD:")
log("Magic ID (0x0-0x3): \"" + (head_id) + "\"")
log("Lumps    (0x4-0x7): \"" + str(head_numlumps) + "\"")
log("DirPtr *(0x8-0x11): \"" + str(head_infotableofs) + "\"")

if str(head_id) == "PWAD":
    print("PWAD FORMAT NOT ACCEPTED. This is a patch file.")
    exit()
if str(head_id) != "IWAD":
    print(head_id)
    print("FILE IS NOT IWAD FORMAT. File must be independent to be configured properly.")
    exit()

# Parse directory

wad_file.seek(head_infotableofs,0)

lumps = 0

while True:
    dir_filepos = int
    dir_size = int
    dir_name = str(8)

    dir_filepos = int.from_bytes(wad_file.read(4), byteorder='little')
    dir_size = int.from_bytes(wad_file.read(4), byteorder='little')
    dir_name = wad_file.read(8).decode('ascii')
    if len(dir_name) != 8:
        break
    log("\nDIR:")
    log("FilePos*(0x0-0x3): \"" + str(dir_filepos) + "\"")
    log("Size    (0x4-0x7): \"" + str(dir_size) + "\"")
    log("Name   (0x8-0x15): \"" + (dir_name) + "\"")
    lumps += 1

log("\nLumps found:" + str(lumps))
dump_file.close()
wad_file.close()