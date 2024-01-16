def with_cache(func):
    def wrapper(self):
        self.get_cache()  # Call the cache updating method
        return func(self)
    return wrapper