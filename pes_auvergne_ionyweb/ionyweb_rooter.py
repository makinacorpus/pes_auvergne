class IonywebRouter(object): 
    def db_for_read(self, model, **hints):
        # "Point all operations on ionyweb models to 'ionywebdb'"
        if model._meta.app_label == 'ionyweb':
            return 'ionywebdb'
        return 'default'

    def db_for_write(self, model, **hints):
        # "Point all operations on ionyweb models to 'ionywebdb'"
        if model._meta.app_label == 'ionyweb':
            return 'ionywebdb'
        return 'default'
    
    def allow_relation(self, obj1, obj2, **hints):
        # "Allow any relation if a both models in ionyweb app"
        if obj1._meta.app_label == 'ionyweb' and obj2._meta.app_label == 'ionyweb':
            return True
        # Allow if neither is ionyweb app
        elif 'ionyweb' not in [obj1._meta.app_label, obj2._meta.app_label]: 
            return True
        return False
    
    def allow_syncdb(self, db, model):
        if db == 'ionywebdb' or model._meta.app_label == "ionyweb":
            return False # we're not using syncdb on our legacy database
        else: # but all other models/databases are fine
            return True