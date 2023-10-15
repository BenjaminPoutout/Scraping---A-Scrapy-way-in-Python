# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class BookscraperPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        field_names = adapter.field_names()
        for field_name in field_names:
            if field_name != 'description':
                value = adapter.get(field_name)
                adapter[field_name] = value.strip()

        lower_case_keys = ['category', 'product_type']
        for lower_case_key in lower_case_keys:
            value = adapter.get(lower_case_key)
            adapter[lower_case_key] = value.lower()

        price_keys = ['price', 'price_excl_tax', 'price_incl_tax', 'tax']
        for price_key in price_keys:
            value = adapter.get(price_key)
            value = value.replace('£', '')
            adapter[price_key] = float(value)

        availability_string = adapter.get('availability')
        split_string_array = availability_string.split('(')
        if len(split_string_array) < 2:
            adapter['availability'] = 0
        else:
            availability_array = split_string_array[1].split(' ')
            adapter['availability'] = int(availability_array[0])

        num_reviews_string = adapter.get('num_reviews')
        adapter['num_reviews'] = int(num_reviews_string)
        
        star_string = adapter.get('stars')
        split_string_star_array = star_string.split(' ')
        star_array = split_string_star_array[1].lower()
        if star_array == "zero":
            adapter['stars'] = 0
        if star_array == "one":
            adapter['stars'] = 1
        if star_array == "two":
            adapter['stars'] = 2
        if star_array == "three":
            adapter['stars'] = 3
        if star_array == "four":
            adapter['stars'] = 4
        if star_array == "five":
            adapter['stars'] = 5
            
        return item