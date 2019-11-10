regis_session = ['name','phone','email']
buying_session = ['select','addcart','payment']
q_a = ['asking','Questioning','checking']

user = {
    '1':'select',
    '2':'payment',
    '3':'name',
    '4':'asking'
}

all_sess = [regis_session,buying_session,q_a]





def checksess(session):
    def dec_repeat(func):
        def wrapper(name,*args,**kwargs):
            for i in session:
                for j,val in enumerate(i):
                    if name == val:
                        try:
                            name = i[j+1]
                        except:
                            name = "finish already"
                        return func(name,*args,**kwargs)

            else:
                print("Please Select Session")

        return wrapper
    return dec_repeat


@checksess(all_sess)
def buying_session(name):
    return "{} is next".format(name)




next_ = buying_session(user['1'])

for i,j in user.items():
    print(i + " is on " + j +" session . " + buying_session(user[i]))
