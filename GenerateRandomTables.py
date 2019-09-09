from SQLServerConnect import SQL
import RandomInventoryTable as rit
import Config as cg
import Queries as qr
import Log as log



class GenerateRandomTables:

	def __init__(self, sql=None, gui=None, sites=None, num_outputs=None, output = None, sqrt_value=None):
		self.sql = sql
		self.sites = sites
		self.gui = gui
		self.output_location = output
		self.num_outputs = num_outputs
		self.sqrt_value = sqrt_value

	def intial_setup(self, sql, gui):
		self.sql = sql
		self.gui = gui

	def final_setup(self, sites, output, num_entries, sqrt_value):  # setup for when the generator random table button is pressed
		self.sites, self.num_outputs, self.output_location, self.sqrt_value = sites, num_entries, output, sqrt_value

	def check_for_all_variable(self):
		if self.sites is None and self.num_outputs is None and self.output_location is None:
			self.gui.error_message(title='Generate Random Table error', message='GRT does not have all the information it needs.')
			exit()

	def create_file_name(self, site):
		if self.output_location == '':
			raise Exception('Cannot have an empty output file')
		return self.output_location + '/' + site + ' - ' + cg.site_location[site] + '.xlsx'

	def reset_progressbar(self):
		self.gui.bar['value'] = 0
		self.gui.update_idletasks()
		self.gui.update()

	def update_progressbar(self,i):
		self.gui.bar['value'] = 100 * (i + 1) / (len(self.sites))
		self.gui.update_idletasks()

	def generate_tables(self):
		self.check_for_all_variable()
		self.reset_progressbar()
		sites_with_num_outputs_less_than = []

		for i in range(len(self.sites)):
			log.message('start: creation of rit with site location {}'.format(self.sites[i]))
			df = self.sql.query_and_export(qr.get_query_text_all_data_on_site(self.sites[i]))
			random_table_generator = rit.RandomInventory(df=df,
			                                             output_file_location=self.create_file_name(self.sites[i]),
			                                             col_name_material_no='material_number',
			                                             col_name_material_desc='material_desc',
			                                             col_name_num_parts='total', col_name_total_value='value',
			                                             col_name_storage_location='storage_location',
			                                             col_name_currency='currency', col_name_batch='batch',
			                                             col_name_plant='plant',
			                                             num_of_outputs=self.num_outputs)

			if random_table_generator.df_large_enough() and random_table_generator.zero_values_on_materials():
				if random_table_generator.not_enough_table_entries():
					sites_with_num_outputs_less_than.append(self.sites[i] + ' - ' + cg.site_location[self.sites[i]])
				random_table_generator.produce_random_table()


			elif not random_table_generator.df_large_enough():
				log.warning_message('the site {} returns null query. Therefore it has been skipped'.format(self.sites[i]))
			else:
				log.message('error: the sites {} has no monentary value on it\'s materials. Therefore, a weight randomization cannot be done'.format(self.sites[i]))
			log.message('end: creation of rit with site location {}'.format(self.sites[i]))
			self.update_progressbar(i)

		if len(sites_with_num_outputs_less_than) != 0:
			message = 'The following sites have less than {} materials, so all of there materials numbers were included.\n\n'.format(self.num_outputs)
			for x in sites_with_num_outputs_less_than:
				message += x + '\n'
			self.gui.message(title='All Materials Included', message=message)
		else:
			self.gui.message(title='Complete', message='All tables have been generated!')
