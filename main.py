import src.extracting as ext
import src.transforming as tr


# Extracting 

film = ext.csv_read('data_marvel')

sales_2008 = ext.csv_read('sales_2008')
sales_2009 = ext.csv_read('sales_2009')
sales_2010 = ext.csv_read('sales_2010')
sales_2011 = ext.csv_read('sales_2011')
sales_2012 = ext.csv_read('sales_2012')
sales_2013 = ext.csv_read('sales_2013')
sales_2014 = ext.csv_read('sales_2014')
sales_2015 = ext.csv_read('sales_2015')
sales_2016 = ext.csv_read('sales_2016')
sales_2017 = ext.csv_read('sales_2017')
sales_2018 = ext.csv_read('sales_2018')
sales_2019 = ext.csv_read('sales_2019')
sales_2020 = ext.csv_read('sales_2020')
sales_2021 = ext.csv_read('sales_2021')


# Transforming 

film = tr.film_creator(film)

df_08 = tr.comics_creator(sales_2008,'2008')
df_09 = tr.comics_creator(sales_2009, '2009')
df_10 = tr.comics_creator(sales_2010, '2010')
df_11 = tr.comics_creator(sales_2011, '2011')
df_12 = tr.comics_creator(sales_2012, '2012')
df_13 = tr.comics_creator(sales_2013, '2013')
df_14 = tr.comics_creator(sales_2014, '2014')
df_15 = tr.comics_creator(sales_2015, '2015')
df_16 = tr.comics_creator(sales_2016, '2016')
df_17 = tr.comics_creator(sales_2017, '2017')
df_18 = tr.comics_creator(sales_2018, '2018')
df_19 = tr.comics_creator(sales_2019, '2019')
df_20 = tr.comics_creator(sales_2020, '2020')
df_21 = tr.comics_creator(sales_2021, '2021')


tr.join_df([
    df_08, df_09, df_10,
    df_11, df_12, df_13,
    df_14, df_15, df_16,
    df_17, df_18, df_19, 
    df_20, df_21], 
    name = 'box_office_comics' 
)

characters_08 = tr.box_characters_creator(df_08, tr.check_list, '2008')
characters_09 = tr.box_characters_creator(df_09, tr.check_list, '2009')
characters_10 = tr.box_characters_creator(df_10, tr.check_list, '2010')
characters_11 = tr.box_characters_creator(df_11, tr.check_list, '2011')
characters_12 = tr.box_characters_creator(df_12, tr.check_list, '2012')
characters_13 = tr.box_characters_creator(df_13, tr.check_list, '2013')
characters_14 = tr.box_characters_creator(df_14, tr.check_list, '2014')
characters_15 = tr.box_characters_creator(df_15, tr.check_list, '2015')
characters_16 = tr.box_characters_creator(df_16, tr.check_list, '2016')
characters_17 = tr.box_characters_creator(df_17, tr.check_list, '2017')
characters_18 = tr.box_characters_creator(df_18, tr.check_list, '2018')
characters_19 = tr.box_characters_creator(df_19, tr.check_list, '2019')
characters_20 = tr.box_characters_creator(df_20, tr.check_list, '2020')
characters_21 = tr.box_characters_creator(df_21, tr.check_list, '2021')

tr.join_df(
    [characters_08, characters_09, characters_10, 
    characters_11, characters_12, characters_13,
    characters_14, characters_15, characters_16,
    characters_17, characters_18, characters_19,
    characters_20, characters_21], 
    name='box_office_characters'
)