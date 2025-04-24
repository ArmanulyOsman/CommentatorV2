import pandas as pd
import Credentials

class Credentials:
    def __init__(self, phone_number=None, password=None, username=None, product=None, reviews=None):
        self.phone_number = phone_number
        self.password = password
        self.username = username
        self.query = product
        self.comments = reviews if reviews is not None else []

    def __repr__(self):
        return (f"Credentials(phone_number='{self.phone_number}', "
                f"password='{self.password}', "
                f"username='{self.username}', "
                f"product='{self.query}', "
                f"reviews={self.comments})")

    def to_dict(self):
        return {
            'phone_number': self.phone_number,
            'password': self.password,
            'username': self.username,
            'product': self.query,
            'reviews': self.comments
        }


def extract_data_from_excel(file_path) -> Credentials:
    # Чтение Excel-файла
    df = pd.read_excel(file_path)

    # Извлечение данных
    phone_number = df.iloc[0, 0] if len(df) > 0 else None
    password = df.iloc[1, 0] if len(df) > 1 else None
    username = df.iloc[2, 0] if len(df) > 2 else None
    product = df.iloc[3, 0] if len(df) > 3 else None
    reviews = df.iloc[:, 1].dropna().tolist()

    # Создание и возврат объекта Credentials
    return Credentials(
        phone_number=phone_number,
        password=password,
        username=username,
        product=product,
        reviews=reviews
    )
