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

#Basic static things for this script
afro_packages = ('afro', 'cat', 'main')
main_page = "https://vel2006.github.io/AfroLinux/allPackages.html"
options = ("add", "remove", "update", "version", "find", "list")
packages_file = "/etc/AfroLinux/packages.json"

#Method for getting values inbetween certain strings / chars
def GetInbetween(text_in: str, start_point: str, end_point: str):
	start_index = text_in.find(start_point)
	end_index = text_in.find(end_point, start_index + len(start_point))
	if start_index != -1 and end_index != -1:
		return text_in[start_index + len(start_point):end_index]

#Method for downloading / getting a web-pages content (that doesnt enforce HTTPv2 rules)
def GetPageContent(site_page: str, content_or_data: bool):
	request = requests.get(site_page)
	match request.status_code:
		case 404:
			print(f"{ERRR_HEAD}Page \'{site_page}\' has returned a 404 error.\n{INFO_HEAD}Try again later.")
			exit()
		case 1015:
			print(f"{ERRR_HEAD}Page \'{site_page}\' has returned a 1015 error.\n{INFO_HEAD}You are likely being rate-limited due to lots of usage, try again in three hours.")
			exit()
		case 403:
			print(f"{ERRR_HEAD}Page \'{site_page}\' has returned a 403 error.\n{INFO_HEAD}You are likely being denied access, or are being re-routed.")
			exit()
		case 200:
			if content_or_data:
				return request.text
			return request.content

#Method for downloading a package onto this system
def DownloadPackage(package_name: str, package_version: int, input_device_packages: dict):
	page_response = GetPageContent(f"https://vel2006.github.io/AfroLinux/{package_name}.xz", False)
	with open(".temp", 'wb') as temp_file:
		temp_file.write(page_response)
		temp_file.close()
	with lzma.open(".temp", 'rb') as in_file:
		with open(f"/etc/AfroLinux/{sys.argv[2]}", 'wb') as out_file:
			shutil.copyfileobj(in_file, out_file)
			out_file.close()
		in_file.close()
	os.remove(".temp")
	device_packages[package_name] = package_version
	with open('/etc/AfroLinux/packages.json', 'w') as file:
		json.dump(input_device_packages, file, indent=4)
		file.close()

def RemovePackage(package_name: str, input_device_packages: dict):
    try:
        os.remove(f"/etc/AfroLinux/{package_name}")
    except FileNotFoundError:
        print(f"{ERRR_HEAD}Package '{package_name}' not found.")
        return

    
    del input_device_packages[package_name]
    with open('/etc/AfroLinux/packages.json', 'w') as file:
        json.dump(input_device_packages, file, indent=4)
        file.close()

    print(f"{INFO_HEAD}Package '{package_name}' removed successfully.")
	
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
				print(f"{INFO_HEAD}Format to use is this:\n{INFO_HEAD}\tafro <add/remove/update/version/find/list> <package>\n{INFO_HEAD}\'list\' options:\n{INFO_HEAD}\t<all/afro>")
				exit()
			case "add" | "remove" | "update" | "version" | "find" | "list":
				print(f"{ERRR_HEAD}The argument \'{sys.argv[1]}\' requires a package as third argument.\n{INFO_HEAD}Use \'--help\' for assistance.")
				exit()
			case _:
				print(f"{ERRR_HEAD}The argument \'{sys.argv[1]}\' is not recognized.\n{INFO_HEAD}Use \'--help\' for assistance.")
				exit()
	case 3:
		#Checking to make sure that the first argument is valid
		if sys.argv[1] not in options:
			print(f"{ERRR_HEAD}The argument \'{sys.argv[1]}\' is not recognized.\n{INFO_HEAD}Use \'--help\' for assistance.")
			exit()
		#Getting a page request to where the information for the packages is held
		response_from_page = GetPageContent(main_page, True)
		#Extracting the packages from the page
		packages = {}
		for line in GetInbetween(response_from_page.text, "<body>", "</body>").splitlines():
			if "<p>" in line:
				packages[GetInbetween(line, "<p>", "=")] = GetInbetween(line, "=", "</p>")
		#Checking to see if the package requested is even inside of the page's contents
		if sys.argv[2] not in packages:
			print(f"{ERRR_HEAD}Unknown package \'{sys.argv[2]}\'.\n{INFO_HEAD}Use \'list all\' for all packages.")
			exit()
		package_version = packages[{sys.argv[2]}]
		#Getting the packages on current device
		device_packages = None
		with open(packages_file, 'r') as file:
			device_packages = json.load(file)
			file.close()
		#Acting acording to the first argument
		match sys.argv[1]:
			#Adding a packages
			case "add":
				if sys.argv[2] in device_packages:
					print(f"{ERRR_HEAD}Package {sys.argv[2]} already installed.\n{INFO_HEAD}For updating use \'update\' not \'add\'.")
					exit()
				#Getting the packge added to this system
				DownloadPackage({sys.argv[2]}, package_version, device_packages)
				print(f"{INFO_HEAD}Package \'{sys.argv[2]}\' was downloaded.")
			#Listing all packages of given type
			case "list":
				match sys.argv[2]:
					case "all":
						print("All Avalable Packages / Tools:")
						for package in packages:
							print(f"{package}: {packages[package]}")
						exit()
					case "afro":
						print("Afro Custom Packages:")
						for package in afro_packages:
							try:
								print(f"{package}: {packages[package]}")
							except:
								print(f"{ERRR_HEAD}Package: {package} is no longer found or supported.")
					case _:
						print(f"{ERRR_HEAD}Package type \'{sys.argv[2]}\' was not found.\n{INFO_HEAD}Use \'--help\' for assistance.")
						exit()
			case "remove":
				if sys.argv[2] in device_packages:
					RemovePackage({sys.argv[2]}, device_packages)
					print(f"{INFO_HEAD}Package \'{sys.argv[2]}\' was removed.")
				else:
					print(f"{ERRR_HEAD}Package \'{sys.argv[2]}\' is not installed.")
					exit()
				
	case _:
		print(f"{ERRR_HEAD}Unknown amount of arguments.\n{INFO_HEAD}Use \'--help\' for assistance.")
