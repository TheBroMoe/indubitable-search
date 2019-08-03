from abc import ABC, abstractmethod 


class Interface(ABC):
    
    def display_title(self):
        pass

    def init_data_struct(self):
        pass

    def start(self):
        pass
    
    def session(self):
        pass
    
    def get_job_title(self):
        pass
    
    def city_search(self):
        pass
    
    def page_search(self):
        pass

    def get_city_set(self):
        pass

    def create_url(self):
        pass
    
    def display_job(self):
        pass
    
    def prompt_user_selection(self):
        pass
    
    def write_to_csv(self):
        pass