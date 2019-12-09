from collections import defaultdict

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.network.urlrequest import UrlRequest
from pprint import pprint
from kivy.clock import Clock


access_token = ''
base_url = 'https://api.youneedabudget.com/v1'
header = {
    'Authorization': f'Bearer {access_token}',
    'Accept': 'application/json',
}

def got_json(req, result):
    # for key, value in result['headers'].items():
    #     print('{}: {}'.format(key, value))
    print(result)
    return result


class YNAB(BoxLayout):

    def __init__(self, **kwargs):
        super(YNAB, self).__init__(orientation='vertical', **kwargs)
        self.category_data = defaultdict(dict)
        self.current_category_group = None
        self.get_categories()
        # while True:
        #     if self.category_data:
        #         break
        # self.rotate_categories(None)

    def parse_categories(self, req, result):
        for group in result['data']['category_groups']:
            group_name = group['name']
            if group_name.startswith('Hidden'):
                continue
            for category in group['categories']:
                category_name = category['name']
                balance = category['balance'] / 1000
                self.category_data[group_name][category_name] = balance
                print(f"{group_name} : {category_name} : {balance}")
        print(self.category_data)

    def rotate_categories(self, dt):
        self.clear_widgets()
        groups = list(self.category_data)
        print(self.category_data)
        current_group = groups[0] if not self.current_category_group else self.current_category_group
        categories = self.category_data[current_group]
        for category in categories:
            balance = self.category_data[current_group][category]
            label = f'{current_group}:{category} balance = ${balance}'
            label = Button(text=label)
            self.add_widget(label)

        current_group_index = groups.index(current_group)
        self.current_category_group = groups[current_group_index + 1] if len(groups) - 1 > current_group_index else groups[0]


    def get_user(self):
        url = f'{base_url}/user'
        req = UrlRequest(
            url, on_success=got_json, on_error=got_json, on_failure=got_json,
            req_headers=header,
        )
    def get_budgets(self):
        url = f'{base_url}/budgets'
        req = UrlRequest(
            url, on_success=got_json, on_error=got_json, on_failure=got_json,
            req_headers=header,
        )

    def get_categories(self, budget_id='last-used'):
        url = f'{base_url}/budgets/{budget_id}/categories'
        UrlRequest(
            url, on_success=self.parse_categories,
            req_headers=header,
        )

class FamilyDashboard(GridLayout):
    def __init__(self, **kwargs):
        super(FamilyDashboard, self).__init__(**kwargs)
        self.cols = 1
        y = YNAB()
        self.add_widget(y)
        Clock.schedule_interval(y.rotate_categories, 10)

class FamilyDashApp(App):
    def build(self):
        return FamilyDashboard()

if __name__ == '__main__':
    FamilyDashApp().run()