class User:
    def __init__(self, user_id, username, lang, reg_date, gen_avail, gen_done, gen_trial, ref_code, refs):
        self.user_id = user_id
        self.username = username
        self.lang = lang
        self.reg_date = reg_date
        self.gen_avail = gen_avail
        self.gen_done = gen_done
        self.gen_trial = gen_trial
        self.ref_code = ref_code
        self.refs = refs


class Generation:
    def __init__(self, user_id, status, input_url, result_url, date, mode, body_type):
        self.user_id = user_id
        self.status = status
        self.input_url = input_url
        self.result_url = result_url
        self.date = date
        self.mode = mode
        self.body_type= body_type
