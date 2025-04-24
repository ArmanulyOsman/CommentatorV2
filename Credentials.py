
class Credentials:
    def __init__(self, phone_number=None, password=None, username=None, product=None, reviews=None):
        self.phone_number = phone_number
        self.password = password
        self.username = username
        self.product = product
        self.reviews = reviews if reviews is not None else []

    def __repr__(self):
        return (f"Credentials(phone_number='{self.phone_number}', "
                f"password='{self.password}', "
                f"username='{self.username}', "
                f"product='{self.product}', "
                f"reviews={self.reviews})")

    def to_dict(self):
        return {
            'phone_number': self.phone_number,
            'password': self.password,
            'username': self.username,
            'product': self.product,
            'reviews': self.reviews
        }
