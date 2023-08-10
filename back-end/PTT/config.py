import mysql.connector
import pandas as pd
host = '127.0.0.1'
user = 'root'
password = '109403502'
database = 'communews'
charset =  "utf8"

def create_table():
    connection = mysql.connector.connect(host=host, user=user, password=password, database=database, charset=charset)
    cursor = connection.cursor()

    create_table_query = '''
        CREATE TABLE IF NOT EXISTS `communews`.`tb_ptt_data` (
        `id_ptt_data` INT NOT NULL AUTO_INCREMENT,
        `subtopic` VARCHAR(45) NOT NULL,
        `title` VARCHAR(200) NOT NULL,
        `link` VARCHAR(400) NOT NULL,
        `date` DATE NOT NULL,
        `page` INT NOT NULL,
        PRIMARY KEY (`id_ptt_data`))
        ENGINE = InnoDB;
    '''
    cursor.execute(create_table_query)
    cursor.fetchall()  # 處理結果集
    connection.commit()

    create_table_query = '''
        CREATE TABLE IF NOT EXISTS `communews`.`tb_ptt_search_link` (
        `id_ptt_link` INT NOT NULL,
        `id_subtopic` INT NOT NULL,
        `ptt_url` VARCHAR(400) NOT NULL,
        `subtopic` VARCHAR(45) NOT NULL,
        `page` INT NOT NULL,
        PRIMARY KEY (`id_ptt_link`))
        ENGINE = InnoDB;
    '''
    cursor.execute(create_table_query)
    cursor.fetchall()  # 處理結果集
    connection.commit()

    create_table_query = '''
        CREATE TABLE IF NOT EXISTS `communews`.`tb_subtopic` (
        `id_subtopic` INT NOT NULL,
        `subtopic_value` VARCHAR(45) NOT NULL,
        PRIMARY KEY (`id_subtopic`))
        ENGINE = InnoDB;
    '''
    cursor.execute(create_table_query)
    cursor.fetchall()  # 處理結果集
    connection.commit()

    cursor.close()
    connection.close()



def read_ptt_link_search_data_from_excel():
    ptt_url_data = 'PTT\data\ptt_search_link.xlsx'
    df = pd.read_excel(ptt_url_data)
    selected_columns = ['ID_PTT_URL', 'ID_Sub_Topic', 'PTT_URL','Sub_Topic','Page']
    ptt_link_data_list = df[selected_columns].values.tolist()
    
    messages = []

    for ptt_link_data in ptt_link_data_list:
        messages.append({'id_ptt_link':ptt_link_data[0],'id_subtopic':int(ptt_link_data[1]),'ptt_url':ptt_link_data[2],'subtopic':ptt_link_data[3],'page':int(ptt_link_data[4])},)

    print(messages)

    connection = mysql.connector.connect(host=host, user=user, password=password, database=database, charset=charset)

    cursor = connection.cursor()

    for message in messages:
        insert_query = '''
            INSERT INTO tb_ptt_search_link (id_ptt_link,id_subtopic, ptt_url, subtopic, page)
            VALUES (%s, %s, %s, %s, %s)
        '''
        data = (message['id_ptt_link'], message['id_subtopic'], message['ptt_url'], message['subtopic'], message['page'])

        cursor.execute(insert_query, data)

    connection.commit()
    connection.close()

def read_ptt_subtopic_id_data_from_excel():
    subtopic_data = 'PTT\data\subtopic_id.xlsx'
    df = pd.read_excel(subtopic_data)
    selected_columns = ['subtopic_id', 'subtopic_value']
    subtopic_data_list = df[selected_columns].values.tolist()
    messages = []

    for subtopic_data in subtopic_data_list:
        messages.append({'id_subtopic':int(subtopic_data[0]),'subtopic_value':subtopic_data[1]})

    print(messages)

    connection = mysql.connector.connect(host=host, user=user, password=password, database=database, charset=charset)

    cursor = connection.cursor()

    for message in messages:
        insert_query = '''
            INSERT INTO tb_subtopic (id_subtopic,subtopic_value)
            VALUES (%s, %s)
        '''
        data = (message['id_subtopic'], message['subtopic_value'])

        cursor.execute(insert_query, data)

    connection.commit()
    connection.close()


#create_table()
#read_ptt_link_search_data_from_excel()
#read_ptt_subtopic_id_data_from_excel()