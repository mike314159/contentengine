


class TextDocument():
    def __init__(self, id, content, metadata):
        self.id = id
        self.content = content
        self.metadata = metadata

    def get_id(self):
        return self.id

    def get_content(self):
        return self.content

    def get_metadata(self):
        return self.metadata

    # def print_summary(self):
    #     print("URI: ", self.uri)
    #     print("Content: ", self.page_content[0:30])
    #     print("Metadata: ", self.metadata)

        