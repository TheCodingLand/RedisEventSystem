import fastText

class worker():

    def __init__(self):
        print("initialized")

    def run(self,data):
        print (f"parsed sentence {data}")
        ft = fastText.load_model('./model/model.ftz')
        result = ft.predict(data['text'],data['nbofresults'])  
        return result[0][1]

