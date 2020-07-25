import json

with open('data/translated_labels.json') as json_file:
    translated_labels = json.load(json_file)

class translator_class():
    def __init__(self):
        self.translated_labels = translated_labels
        self.language_used = 'english'
        self.get_inverse_dic()

    def get_inverse_dic(self):
        self.inverse_dic = {}
        for original_item in self.translated_labels:
            translated_item = self.translated_labels.get(original_item).get(self.language_used, 'failed_item')
            self.inverse_dic[translated_item] = original_item

    def translate(self, item):
        return self.translated_labels.get(item, {}).get(self.language_used, item)

    def translate_list(self, list_items):
        return [self.translate(item) for item in list_items]
    
    def to_original(self, translated_item):
        return self.inverse_dic.get(translated_item, translated_item)
    
    def to_original_list(self, list_items):
        return [self.to_original(item) for item in list_items]


if __name__ == '__main__':
    translator = translator_class()
    print(translator.translate('COLE_BILINGUE'))

