import src.services as services



from src.database import Database


class Controller:
    def __init__(self, conf):
        self.database = Database(conf)


    def fill_trigger(self):
        object_list = self.database.select('WallPost')

        triggers_objs_list = self.database.select('TriggerWord')

        triggers_words_list = {x['Name']: x['TriggerId'] for x in triggers_objs_list}

        for obj in object_list:
            if len(obj['Text']) != 0:
                catchted_triggers_name_list = services.trigger_check(obj['Text'], triggers_words_list)
                if len(catchted_triggers_name_list) > 0:
                    obj['IsTarget'] = True
                    self.database.update_record(obj)
                print('The trigger check on WallPost %s completed' % obj['WallPostId'])
                '''catchted_triggers_ind_list = [triggers_words_list[i] for i in catchted_triggers_name_list]
                for ind in catchted_triggers_ind_list:
                    self.database.set_wall_post_trigger({"WallPostId": obj['WallPostId'], "TriggerId": ind})'''


    def fill_emotion(self):
        object_list = self.database.select('Comment')
        for obj in object_list:
            if len(obj['Text']) != 0:
                obj['EmotionMark'] = services.fill_rec_emotions(obj['Text'])
                self.database.update_commit_record(obj)
                print('The emotion check on Comment %s completed' % obj['CommentId'])




if __name__ == "__main__":
    from config_parser import Config

    config = Config("../configs.yaml")
    controller = Controller(config.database)
    controller.fill_emotion()
    controller.fill_trigger()