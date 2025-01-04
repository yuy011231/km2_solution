class Config:
    _app_name = "km2 itc solution"
    _app_initial_window_size = "800x500"
    _font_type = "Helvetica"

    @classmethod
    def initialize(cls):
        pass

    @classmethod
    def app_name(cls):
        return cls._app_name
    
    @classmethod
    def app_initial_window_size(cls):
        return cls._app_initial_window_size
    
    @classmethod
    def font_type(cls):
        return cls._font_type
