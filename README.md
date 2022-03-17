# Batch CBR/CBZ Converter
Create CBR (RAR) or CBZ (Zip) file from multiple JPEG or PNG files in the same folder

## Use case scenarios
- There are multiple folders in which JPEG or PNG files are stored
- Create CBR (RAR) or CBZ (Zip) files for each folder

## Pre-requisite
- Python 3 is installed on the host
- RAR, UNRAR (WinRAR) and 7-zip are installed somewhere on the host
- Parameters are configured within config.json file

## Known issues, To-do items
### Pack
- Tentatively multiprocessing support removed (to fix path issues)
- Multi-byte character support
### Unpack
- Multi-byte character support
