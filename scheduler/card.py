class CardData:
    def __init__(self, card_number, account_number, exp_date_str, cpr, dob, rim, phone):
        self.card_number = card_number
        self.account_number = account_number
        self.exp_date_str = exp_date_str
        self.dob = dob
        self.cpr = cpr
        self.rim = rim
        self.phone = phone
        
    #check if card is having all valid attributes 
    def is_valid_card(self):
        is_valid = True
        dictionary = self.__dict__
        for k,v in dictionary.items(): 
            if dictionary[k] is None:
                is_valid = False 
        return is_valid
