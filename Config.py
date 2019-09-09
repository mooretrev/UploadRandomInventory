import sys
import os

executed = False
site_location = dict()
site_location_keys = []
site_location_values = []
site_location_length = 0


def setup(sql):
	global executed, site_location, site_location_keys, site_location_values
	executed = True
	df = sql.query_and_export('select Park_Name, SAP_Plant from Parks where Country_ID = 840 and SAP_Plant is not null order by SAP_Plant')
	site_location_values = df.iloc[:,0]
	site_location_keys = df.iloc[:,1]
	create_dict()


def create_dict():
	global site_location_length
	for i in range(len(site_location_keys)):
		site_location[site_location_keys[i]] = site_location_values[i]
		site_location_length += 1


def get_site_location_dict():
	global site_location
	check_if_setup()
	return site_location


def get_site_location_keys():
	global site_location_keys
	check_if_setup()
	return site_location_keys


def get_site_location_values():
	global site_location_values
	check_if_setup()
	return site_location_values


def get_site_location_length():
	global site_location_length
	check_if_setup()
	return site_location_length


def check_if_setup():
	if not executed:
		raise Exception('The config class has to be setup before it can be called. Coding Error')

def resource_path(relative_path):
	if hasattr(sys, '_MEIPASS'):
		return os.path.join(sys._MEIPASS, relative_path)
	return os.path.join(os.path.abspath("."), relative_path)


EDPR_logo_location = resource_path('EDPR_logo.bmp')
icon_location = resource_path("icon.ico")
export_template = resource_path('Random Inventory Template.xlsx')


