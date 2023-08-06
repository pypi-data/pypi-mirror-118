import zipfile


class newzip:
    def __init__(self, name, number, file='', files='', numbers=0):
        self.name = name
        self.number = number
        self.file = file
        self.files = files
        self.numbers = numbers

    def new_zip(self):
        new = zipfile.ZipFile(self.name, 'w')
        if int(self.number) > 1:
            new.write(f'{self.file}')
            new.write(f'{self.files}')
        else:
            new.write(f'{self.file}')

    def new_zips(self):
        jshu = 0
        for i in range(self.numbers):
            jshu += 1
            if int(jshu) == 0 or 1:
                new = zipfile.ZipFile(f'{self.name}', 'w')
                if self.files == '':
                    new.write(f'{self.file}')
                else:
                    new.write(f'{self.file}')
                    new.write(f'{self.files}')
                print(f"{self.name}")
            news = zipfile.ZipFile(f"{jshu}{self.name}", 'w')
            print(f"{jshu}{self.name}")
            if int(self.number) > 1:
                news.write(f'{self.files}')
                news.write(f'{self.file}')
            else:
                news.write(f'{self.file}')
