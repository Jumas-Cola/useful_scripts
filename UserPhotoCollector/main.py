from UserPhotoCollector import UserPhotoCollector


if __name__ == '__main__':
    token = '123456789123456789123456789123456789'
    session = UserPhotoCollector(token, 123456789, 'surname')
    session.dump()
