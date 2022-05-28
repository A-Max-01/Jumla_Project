from django.core.paginator import Paginator


class MyPaginator:
    def __init__(self, object_list, number_items):
        self.object_list = object_list
        self.number_items = number_items
        self.items = Paginator(self.object_list, self.number_items)
        self.page_nums = None
        self.pages = None

    def get_pages(self, page):
        self.page_nums = "a" * self.items.get_page(page).paginator.num_pages
        self.pages = self.items.get_page(page)
        return self.page_nums, self.pages
