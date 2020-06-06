import src.services as services

class Controller:

    def fill_trigger(self, database):
        object_list = database.select('WallPost')

        triggers_objs_list = database.select('TriggerWord')

        triggers_words_list = {x['Name']: x['TriggerId'] for x in triggers_objs_list}

        for obj in object_list:

            catchted_triggers_name_list = services.trigger_check(obj['Text'], triggers_words_list)

            if len(catchted_triggers_name_list) > 0:
                obj['IsTarget'] = True
                database.update_record(obj)

            print('The trigger check on WallPost %s completed' % obj['WallPostId'])
            '''catchted_triggers_ind_list = [triggers_words_list[i] for i in catchted_triggers_name_list]
            for ind in catchted_triggers_ind_list:
                self.database.set_wall_post_trigger({"WallPostId": obj['WallPostId'], "TriggerId": ind})'''


    def fill_emotion(self, database):
        object_list = database.select('Comment')
        for obj in object_list:
            obj['EmotionMark'] = services.fill_rec_emotions(obj['Text'])
            database.update_commit_record(obj)
            print('The emotion check on Comment %s completed' % obj['CommentId'])
