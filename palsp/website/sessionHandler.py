import time, datetime, threading, hashlib, random

class SessionHandler:
    def __init__(self):
        self.session_list = []

    def is_active_session(self, user_hash):
        for session in self.session_list:
            if session.session_id == user_hash:
                session.last_update = datetime.datetime.now()
                return True
        return False
    
    def get_session(self, request):
        user_hash = self.get_user_hash(request)
        for session in self.session_list:
            if session.session_id == user_hash:
                return session
        return None
    
    
    def get_user_hash(self, request):
        return hashlib.md5(str(request.remote_addr+request.headers["User-Agent"]).encode()).hexdigest()

    def create_session(self, user_id, request, expire_time):
        session =  self.Session(self.get_user_hash(request), user_id)
        session.lifetime = expire_time
        self.session_list.append(session)
        return session
    
    def session_is_expired(self, session):
        delta = datetime.datetime.now() - session.last_update
        if int(delta.total_seconds()) > session.lifetime:
            print(f"session with id: {session.session_id} expired and got removed")
            return True
        return False

    def cron_job(self):
        while True:
            for session in self.session_list:
                if self.session_is_expired(session):
                    self.session_list.remove(session)
            time.sleep(5)

    def init_cron_job(self):
        threading.Thread(target=self.cron_job).start()
    
    def authenticate(self, request):
        if self.get_session(request):
            if self.get_session(request).user_id != "guest":
                return True
        return False

    def simple_authenticate(self, request):
        session = self.get_session(request)
        if session != None:
            session.last_update =datetime.datetime.now()
            return True
        return False
    
    def remove_session(self, request):
        for session in self.session_list:
            if session.session_id == self.get_user_hash(request):
                self.session_list.remove(session)
                return
            
    def get_user_id(self, request):
        user_hash = self.get_user_hash(request)
        for session in self.session_list:
            if session.session_id == user_hash:
                return session.user_id
        return ""
    
    def set_accept_content_warning(self, request):
        self.get_session(request).content_warning_accepted = True


    def is_guest(self, request):
        session = self.get_session(request)
        if session != None:
            if session.user_id == "guest":
                return True
        return False

    def create_guest_session(self, request, lifetime=1800):
        session = self.Session(self.get_user_hash(request), "guest")
        session.lifetime = lifetime
        self.session_list.append(session)
        return session

    class Session:
        def __init__(self, session_id, user_id):
            self.session_id = session_id
            self.user_id = user_id
            self.date = datetime.datetime.now()
            self.last_update = datetime.datetime.now()
            self.quota = random.randint(3, 11)
            self.lifetime = 1800
            self.content_warning_accepted = False