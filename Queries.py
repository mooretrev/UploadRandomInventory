'''
This class is define in order to make easier to find and change a query if needed
'''


'''
This query returns the SAP code for the sites that have more than x materials numbers. It is used when the select in querys
button is pressed.
'''
def get_query_text_sites_in_data_more_than_x(x):
	return """
		select sap_code
		from(
		SELECT distinct MATNR as material_no, WERKS as sap_code
		FROM [Park_Analytics].[work_orders].[edpr_Stocks_zmm_sm_xml_s]
		where WAERS = 'USD' and LABST > 0
		)temp
		group by temp.sap_code
		having count(temp.material_no) >= """ + str(x) + """
		order by temp.sap_code
		"""


'''
This query is used in the generate random table class. This query is run once for each selected sites. For a paritucalar 
site the inventory is group by the material number. If there are duplicate material numbers, the number of stock and the 
values of the stock is summed. 

One assumtion I made is that if two material numbers are the same, the material description and the storage location will
be the same as well. I implemented this in my query by using the min functino for the material description and the storage
location.
'''
def get_query_text_all_data_on_site(site):
	return """		
		select 
		stock.id,
		stock.ZMM_SM_XML_S_Id,
		stock.MATNR as material_number, 
		stock.MAKTX_EN as material_desc, 
		stock.LABST as total, 
		stock.SALK3 as value, 
		stock.LGOBE as storage_location, 
		stock.CHARG as batch,
		stock.WAERS as currency,
		stock.WERKS as plant
		from(
			--get raw data from site
			select *
			from work_orders.edpr_Stocks_zmm_sm_xml_s
			where WAERS = 'USD' and LABST > 0 and WERKS = '{}'
		) as stock
		
		join (
			--select most recent material data
			select 
			max(id) as id
			from work_orders.edpr_Stocks_zmm_sm_xml_s
			where WAERS = 'USD' and LABST > 0 and WERKS = '{}'
			group by MATNR
		)as filter_stock
		on stock.id = filter_stock.id
		
		order by SALK3 desc, stock.id desc
		""".format(site, site)

