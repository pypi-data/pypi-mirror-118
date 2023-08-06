import csv
import os
import sys
from datetime import datetime
from itertools import islice
import math

class prism_rerun:
	def __init__(self):
		self.DEV_HISTORY = "Dev History"
		self.CLASS = "Class"
		self.METHOD = "Method"

	def read_csv_as_list_of_dict(self, filename):
		try:
			with open(filename) as csv_file:
				file_data = csv.reader(csv_file, delimiter=',')
				headers = next(file_data)
				return [dict(zip(headers, value)) for value in file_data]
		except FileNotFoundError:
			print("Wrong file or file path")
			print("Exception in re-running Prism")
			sys.exit()			

	def formTextFile(self, csv_list):
		text_content = dict()
		for value in csv_list:
			try:
				if value[self.DEV_HISTORY].split("/")[0] == "0":
					if value[self.CLASS] not in text_content:
						text_content[value[self.CLASS]] = [value[self.METHOD]]
					else:
						text_content[value[self.CLASS]].append(value[self.METHOD])
			except Exception as e:
				print("\nError occurred! Please check this case manually.")
				print("Full row content %s", value)
				print("Exception while parsing the following row %s:%s", value[self.CLASS], value[self.METHOD])
				print()
				continue
		print("Total 0/5 = ",sum([len(val) for key,val in text_content.items()]))
		return text_content

	def write_txt_file(self, txt_file_content, output_filename, split_length):
		with open(output_filename, 'w') as txt_file: 
			for key, value in txt_file_content.items():
				number_of_splits = math.ceil(len(value)/split_length)
				iter_value = iter(value)
				splits = [list(islice(iter_value, elem)) for elem in [split_length]*number_of_splits]
				for split in splits:
					listItems = ",".join(split)
					txt_file.write('%s:%s\n' % (key, listItems))

	def run_multiple_test_cases(self, txt_filename, stop_jobs, chargebee_app_full_path):
		try:

			print("""
Important Notes:
1. If you run one set of test cases first and then if start the second set your first set will be deleted completely. 
2. Do not run any test case independently while the script is running.
3. If your test case main method has any test Methods mentioned then only the mentioned methods will run so please look up for that.
For more details visit https://sites.google.com/a/chargebee.com/cb---qa/home/qa-controller-1/qa-docs-for-developers/running-multiple-testcase-in-order
				""")

			if stop_jobs:
				print("Stopping Jobs")
				os.system("cd && cd " + chargebee_app_full_path + " /tomcat/bin && sh restart.sh jobs stop")

			os.chdir(chargebee_app_full_path)
			os.system("sh scripts/runTestList.sh" + txt_filename)

		except Exception as e:
			print("Exception in re-running Prism")
			sys.exit()

	def rerun(self):
		print("""\n
PRE REQUISITES
1. Checkout to the right branch for which the PRISM RE-REUN should be triggered in local
2. Stash all your local changes
3. Make sure the local build is already completed
4. Stop the running jobs if any""")

		print("""\nEnter your chargebee-app path. 
Eg: /Users/cb-ashwin/work/chargebee-app""")
		chargebee_app_full_path = input()
		try:
			os.chdir(chargebee_app_full_path)
		except:
			print("Invalid path. Exiting...")
			print("Exception in re-running Prism")
			sys.exit()

		print("""\nEnter the csv path.
Eg: /Users/cb-ashwin/Downloads/8478_master_new_failures_with_rerun.csv""")
		filename = input()

		csv_object = self.read_csv_as_list_of_dict(filename)

		txt_file_content = self.formTextFile(csv_object)
		print(txt_file_content)

		output_filename = "prism_test_content_"+str(datetime.now().timestamp()).split(".")[0]+".txt"
		self.write_txt_file(txt_file_content, output_filename, 3)
		print("Parsed test filename = ", output_filename)

		self.run_multiple_test_cases(output_filename, False, chargebee_app_full_path)

		print("\nThe report can be found in " + chargebee_app_full_path + "/qa_data/testReportList/index.html")
