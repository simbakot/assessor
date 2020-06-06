import mysql.connector
from mysql.connector import Error

class Database:

    def __init__(self, config):
        self.host = config['host']
        self.port = config['port']
        self.database = config['database']
        self.user = config['user']
        self.password = config['password']

    def get_db_conn(self):
        conn = mysql.connector.connect(host=self.host,
                                       port=self.port,
                                       database=self.database,
                                       user=self.user,
                                       password=self.password)
        return conn


    def get_trigger_word_list(self, records):
        triggers_objs_list = []
        for row in records:
            triggers_objs_list.append({'TriggerId':  row[0], 'Name': row[1]})

        return triggers_objs_list

    def get_wall_post_list(self, records):
        triggers_objs_list = []

        for row in records:

            obj = {
                'WallPostId': row[0],
                'OuterId': row[1],
                'PublishDateTime': row[2],
                'Text': row[3],
                'WallOwnerOuterId': row[4],
                'OuterAuthorId': row[5],
                'WallPostURL': row[6],
                'LikesQuantity': row[7],
                'RepostQuantity': row[8],
                'CommentQuantity': row[9],
                'ViewsQuantity': row[10],
                'LastModifiedDateTime': row[11],
                'EmotionMark': row[12],
                'IsTarget': row[13],
            }

            triggers_objs_list.append(obj)


        return triggers_objs_list


    def get_comment_list(self, records):
        triggers_objs_list = []

        for row in records:
            obj = {
                'CommentId': row[0],
                'OuterId': row[1],
                'PublishDateTime': row[2],
                'Text': row[3],
                'WallPostId': row[4],
                'OuterAuthorId': row[5],
                'LikesQuantity': row[6],
                'CommentQuantity': row[7],
                'LastModifiedDateTime': row[8],
                'EmotionMark': row[9],
                'IsTarget': row[10]
            }

            triggers_objs_list.append(obj)

        return triggers_objs_list


    def set_wall_post_trigger(self, obj):

        sql = f"""
        INSERT INTO WallPost_Trigger
        (
          WallPostId,
          TriggerId
        )
        VALUES
        (
          '{obj["WallPostId"]}',
          '{obj["TriggerId"]}'
        );"""

        cnx = self.get_db_conn()
        cursor = cnx.cursor()
        cursor.execute(sql)
        cnx.commit()

        cursor.close()
        cnx.close()



    def update_commit_record(self, obj):
        try:

            if obj['EmotionMark'] !=2:
                print(obj['EmotionMark'])
                print(obj['Text'])

            obj['IsTarget'] = True
            conn = self.get_db_conn()
            if conn.is_connected():
                query = f"""
                    UPDATE `Comment` 
                    SET `EmotionMark`={obj['EmotionMark']}     	                     	    
                    WHERE CommentId={obj['CommentId']};
                """
                cursor = conn.cursor()
                cursor.execute(query)
                conn.commit()
        except Error as e:
            print(f"Error when updating emotions mark for Post #{obj['CommentId']}")
            print(e)
        finally:
            #conn.close()
            pass


    def update_record(self, obj):

        try:
            conn = self.get_db_conn()
            if conn.is_connected():
                query = f"""
                    UPDATE WallPost 
                    SET IsTarget={obj['IsTarget']}     	                     	    
                    WHERE WallPostId={obj['WallPostId']};
                """
                cursor = conn.cursor()
                cursor.execute(query)
                conn.commit()
        except Error as e:
            print(f"Error when updating emotions mark for Post #{obj['WallPostId']}")
            print(e)
        finally:
            conn.close()


    def select(self, db_name):
        if db_name == "TriggerWord":
            sql_select_Query = "select * from TriggerWord"

        if db_name == "WallPost":
            sql_select_Query = f"""
                    SELECT *    
                    FROM WallPost
                    WHERE IsTarget IS NULL
                    ORDER BY LastModifiedDateTime desc;"""

        if db_name == 'Comment':
            sql_select_Query = f"""
                                SELECT *    
                                FROM Comment
                                WHERE EmotionMark IS NULL
                                ORDER BY LastModifiedDateTime desc;"""

        try:
            connection = self.get_db_conn()
            cursor = connection.cursor()
            cursor.execute(sql_select_Query)
            records = cursor.fetchall()

            print("Total number of rows in Laptop is: ", cursor.rowcount)

            print("\nPrinting each laptop record")

            #{'TriggerId': 1, 'Name': 'губернатор'}
            if db_name == "TriggerWord":
                return self.get_trigger_word_list(records)
            if db_name == "WallPost":
                return self.get_wall_post_list(records)
            if db_name == 'Comment':
                return self.get_comment_list(records)


        except Error as e:
            print("Error reading data from MySQL table", e)
        finally:
            if (connection.is_connected()):
                connection.close()
                cursor.close()
                print("MySQL connection is closed")


if __name__ == "__main__":
    from config_parser import Config
    config = Config("../configs.yaml")
    db = Database(config.database)
    L = db.select('WallPost')
    print(L)