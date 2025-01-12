class DefaultUtils:
    def remove_html_tags(text: str):
        return text.replace('<', '').replace('>', '')