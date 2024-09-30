class TextFileReaderWriter:
    def read(self, filepath):
            with open(filepath, 'r') as file:
                return file.read()

    def write(self, filepath, content):
        with open(filepath, 'w') as file:
            file.write(content)


file_rw = TextFileReaderWriter()
file_rw.write('sampleOutput.txt', 'I am Don Eleazar T. Fernandez')

content = file_rw.read('sampleOutput.txt')
print(content)