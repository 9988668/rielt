import pandas as pd 
import numpy as np 
import sqlalchemy


def main():

	# create random DataFrame
	data = np.random.choice(np.arange(1000), size=100, replace=False)

	first_df = pd.DataFrame(data, columns = ['Name_Id'])
	first_df['Product_Id'] = np.random.randint(0, 1000, 100)
	first_df['Sales'] = np.random.randint(0, 1000, 100)

	# create engene to sql_DB

	engine = sqlalchemy.create_engine('postgresql://postgres:paedf5l5@localhost/postgres')
	con = engine.connect()
	print(engine.table_names())

	# give name to table and write table to DB

	table_name = 'random_numbers'
	first_df.to_sql(table_name, con, if_exists='append', index=False)

	print(engine.table_names())

	# read table to DataFrame

	df = pd.read_sql_table('random_numbers', engine)
	print(df.head())

	# create query and use query

	query = """
	        select * 
	        from random_numbers 
	        limit 10 ;
	"""
	df = pd.read_sql_query(query,engine)
	print(df)


	con.close()


	# print(first_df)

if __name__ == '__main__':
	main()