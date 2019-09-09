import numpy as np
import pyodbc
from pandas import DataFrame
import LoginInfo


class SQL:
	'''
	This class is how the program connects and runs query through the SQL server. The only function that should be used
	in this class is the query_and_export.
	'''
	def __init__(self):
		self.cursor = self._connect_to_sql_server()

	def _connect_to_sql_server(self):
		cnxn = pyodbc.connect(LoginInfo.login_info)
		cursor = cnxn.cursor()
		return cursor

	def _query(self, select):
		self.cursor.execute(select)

	def _convert_to_data_frame(self):
		#takes in a cursor and returns a df
		column_name = []
		for x in self.cursor.description:
			column_name.append(x[0])
		df = DataFrame(np.array(self.cursor.fetchall()))
		if not df.empty:
			df.columns = column_name
		return df

	def query_and_export(self, select):
		'''
		:param select: This is the query text to be run by the SQL server
		:return: The table from the query as a Date Frame
		This is only function that should be used outside of this class. This function takes in the query text and returns
		the resulting table as a dataframe.
		'''
		self._query(select)
		return self._convert_to_data_frame()




