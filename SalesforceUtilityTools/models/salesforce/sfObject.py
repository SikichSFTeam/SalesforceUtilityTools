import json

class SfObject(object):
    name = ''
    fields = {}

    def __str__(self):
        return json.dumps(self.fields)

    def __setattr__(self, name, value):
        if name in self.fields:
            self.fields[name].value = value
            return True
        else:
            return super().__setattr__(name, value)

    def __getattr__(self, name):
        if name in self.fields:
            return self.fields[name].value
        else:
            return super.__getattr__(name)
        