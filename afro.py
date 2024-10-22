import requests
import shutil
import lzma
import json
import sys
import os

#Message headers
ERRR_HEAD = "[!] ERRR: "
INFO_HEAD = "[i] INFO: "
MISC_HEAD = "[*] MISC: "
INPT_HEAD = "[>] INPT: "

#Method for getting values inbetween certain strings / chars
def GetInbetween(text_in, start_point, end_point):
	start_index = text_in.find(start_point)
	end_index = text_in.find(end_point, start_index + len(start_point))
	if start_index != -1 and end_index != -1:
		return text_in[start_index + len(start_point):end_index]

#Checking the script arguments and acting as needed
match len(sys.argv):
	case 1:
		#Just use --help
		print(f"{ERRR_HEAD}No arguments given.\n{INFO_HEAD}Use \'--help\' for assistance.")
		exit()
	case 2:
		#Dealing with the arguments (likely not the right amount)
		match sys.argv[1]:
			case "--help":
				print(f"{INFO_HEAD}Afro is the custom (and very bad) package manager for Afro Linux.\n{INFO_HEAD}It only works for custom scripts the devs have published on Github under the 'versions' branch for Afro Linux.")
				print(f"{INFO_HEAD}Format to use is this:\n{INFO_HEAD}\tafro <add/remove/update/version/find/list> <package>\n{INFO_HEAD}if using 'list' have 'all' as second argment ex: afro list all")
				exit()
			case "add" | "remove" | "update" | "version" | "find" | "list":
				print(f"{ERRR_HEAD}The argument \'{sys.argv[1]}\' requires a package as third argument.\n{INFO_HEAD}Use \'--help\' for assistance.")
				exit()
			case _:
				print(f"{ERRR_HEAD}The argument \'{sys.argv[1]}\' is not recognized.\n{INFO_HEAD}Use \'--help\' for assistance.")
				exit()
	case 3:
		#Checking to make sure that the first argument is valid
		if sys.argv[1] not in ("add", "remove", "update", "version", "find", "list"):
			print(f"{ERRR_HEAD}The argument \'{sys.argv[1]}\' is not recognized.\n{INFO_HEAD}Use \'--help\' for assistance.")
			exit()
		#Getting a page request to where the information for the packages is held
		response_from_page = requests.get("https://vel2006.github.io/AfroLinux/allPackages.html")
		if response_from_page.status_code != 200:
			print(f"{ERRR_HEAD}Page for holding the packages is down.\n{INFO_HEAD}Check the github rebo\'s version branch and try again later.")
			exit()
		#Extracting the packages from the page
		packages = {}
		for line in GetInbetween(response_from_page.text, "<body>", "</body>").splitlines():
			if "<p>" in line:
				packages[GetInbetween(line, "<p>", "=")] = GetInbetween(line, "=", "</p>")
		#Checking to see if the package requested is even inside of the page's contents
		if sys.argv[2] not in packages:
			print(f"{ERRR_HEAD}Unknown package \'{sys.argv[2]}\'.\n{INFO_HEAD}Use \'list all\' for all packages.")
			exit()
		#Getting the packages on current device
		device_packages = None
		with open("file.json", 'r') as file:
			device_packages = json.load(file)
			file.close()
		#Acting acording to the first argument
		match sys.argv[1]:
			case "add":
				if sys.argv[2] in device_packages:
					print(f"{ERRR_HEAD}Package {sys.argv[2]} already installed.\n{INFO_HEAD}For updating use \'update\' not \'add\'.")
					exit()
				#Getting the packge and decompressing it
				page_response = requests.get(f"https://vel2006.github.io/AfroLinux/{sys.argv[2]}.xz")
				with open(".temp", 'wb') as temp_file:
					temp_file.write(page_response.content)
					temp_file.close()
				with lzma.open(".temp", 'rb') as in_file:
					with open(f"/atc/AfroLinux/{sys.argv[2]}", 'wb') as out_file:
						shutil.copyfileobj(in_file, out_file)
						out_file.close()
					in_file.close()
				os.remove(".temp")
	case _:
		print(f"{ERRR_HEAD}Unknown amount of arguments.\n{INFO_HEAD}Use \'--help\' for assistance.")
