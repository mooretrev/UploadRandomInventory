import random
import math
from OutputToExcel import ExportExcel

class RandomInventory:
	# col_name_plant = self.col_name_plant, col_name_batch = self.col_name_batch, col_name_manufacturer_no = self.col_name_manufactuer_no,
	# col_name_currency = self.col_name_currency, col_name_total_price = self.col_name_total_value)

	def __init__(self, df=None, output_file_location=None, col_name_material_no=None, col_name_material_desc=None, col_name_num_parts=None, col_name_total_value=None, col_name_storage_location=None, col_name_currency=None, col_name_batch=None, col_name_plant=None, num_of_outputs=None, sqrt_value=None):
		self.df = df
		self.output_file_location = output_file_location
		self.col_name_material_no = col_name_material_no
		self.col_name_material_desc = col_name_material_desc
		self.col_name_num_parts = col_name_num_parts
		self.col_name_total_value = col_name_total_value
		self.col_name_storage_location = col_name_storage_location
		self.col_name_currency = col_name_currency
		self.col_name_batch = col_name_batch
		self.col_name_plant = col_name_plant
		self.num_of_outputs_less_than_table_size = False
		self.sqrt_value = sqrt_value
		self.num_of_outputs = self._determine_num_of_outputs(num_of_outputs)
		if sqrt_value:
			self.col_name_sqrt = 'Sqrt: {}'.format(self.col_name_total_value)
			self._sqrt_column(self.col_name_total_value, self.col_name_sqrt)

	def produce_random_table(self):
		if(not self.num_of_outputs_less_than_table_size):
			if self.sqrt_value: randomly_selected_positions = self._generate_random_table_entries(self.col_name_sqrt)
			else: randomly_selected_positions = self._generate_random_table_entries(self.col_name_total_value)
			preped_df = self._prep_table_for_export(randomly_selected_positions)
			self._export_random_table(preped_df)
		else:
			self._export_random_table(self.df)

	def _generate_random_table_entries(self, weighted_col_name):
		i = 0
		num_of_rand_entries_added = 0
		randomly_selected_positions = []
		j = 0
		prev_i = 0
		total_weight = self._get_total_weight()

		while(num_of_rand_entries_added < self.num_of_outputs):
			rand_num = random.randint(1, total_weight)
			while(i == prev_i):
				rand_num = rand_num - self.df.loc[j,weighted_col_name]
				if j not in randomly_selected_positions and rand_num < 0:
					randomly_selected_positions.append(j)
					num_of_rand_entries_added = num_of_rand_entries_added + 1
					i += 1
					break
				j += 1
				j %= self.df.shape[0]
			prev_i = i
		return randomly_selected_positions

	def _prep_table_for_export(self, randomly_selected_positions):
		self.col_name_storage_location
		out = self.df.iloc[randomly_selected_positions]
		out = out.sort_values(self.col_name_total_value, ascending=False)
		return out

	def _export_random_table(self, out):
		ExportExcel(filename=self.output_file_location, df=out, col_name_material_no=self.col_name_material_no,
		            col_name_material_desc=self.col_name_material_desc, col_name_num_parts=self.col_name_num_parts,
		            col_name_total_value=self.col_name_total_value, col_name_storage_location=self.col_name_storage_location,
		            col_name_plant=self.col_name_plant, col_name_batch=self.col_name_batch,
		            col_name_currency=self.col_name_currency, col_name_total_price=self.col_name_total_value)


	def _get_total_weight(self):
		if self.sqrt_value: values = self.df.loc[:, self.col_name_sqrt]
		else: values = self.df.loc[:, self.col_name_total_value]
		return int(values.sum())

	def _determine_num_of_outputs(self, num_of_outputs):
		if self.df.shape[0] >= num_of_outputs:
			return num_of_outputs
		else:
			self.num_of_outputs_less_than_table_size = True
			return self.df.shape[0]

	def _sqrt_column(self, col_name_input, col_name_output):
		for i in range(self.df.shape[0]):
			self.df.loc[i, col_name_output] = int(math.sqrt(self.df.loc[i, col_name_input]))

	def not_enough_table_entries(self):
		return self.num_of_outputs_less_than_table_size

	def zero_values_on_materials(self):
		return self._get_total_weight() > 5

	def df_large_enough(self):
		return self.df.shape[0] > 0










