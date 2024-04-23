from common import replace_ownbrand, remove_currency, perform_request_tesco, \
    reg_replace, remove_string_from_number, standardise, replace_if, generate_insert


class Dunnes():
    def __init__(self, item_names):
        self.item_names = item_names
    """
    The Dunnes class
    """

    def get_unit(self, raw_product):
        raw_unit = raw_product.split("product description")[1].split("€")[2]
        if "each" in raw_unit:
            return float(raw_unit.split("each")[0].strip())
        if "Deal" in raw_unit:
            return float(raw_product.split("product description")[1].split("€")[1].split(" ")[0])

        return float(raw_unit.split("/")[0])

    def remove_garbage(self, raw_product):
        result = []

        unit_price = self.get_unit(raw_product)
        raw_product = raw_product.split("<br/>")[0]
        raw_product = replace_if(raw_product, ["<b>Features</b>"])
        dunnes_product = reg_replace("<br/>", "Cart", raw_product)
        dunnes_product = dunnes_product.replace(",", "").split("€")
        result.append(replace_ownbrand(dunnes_product[0], "dunnes stores"))
        result.append(remove_string_from_number(remove_currency(dunnes_product[1])))
        result.append(unit_price)
        return result

    def format_dict(self, product, cleaned):
        return {
            'brand': "dunnes",
            'category': product,
            'product': cleaned[0],
            'price': cleaned[1],
            'unit_price': cleaned[2],
        }

    def search_product(self, product, is_csv=True):
        """
        Searches for product.
        product = Name of grocery we want.
        is_csv: True, as when I run locally, I want to see it in terminal.
        """
        resp = {
            'products': [],
            'meta': []
        }

        url = f"https://www.dunnesstoresgrocery.com/sm/delivery/rsid/258/results"
        soup = perform_request_tesco(url, {'q': product})
        for row in soup.find_all("div", {"class": "ColListing--1fk1zey bPxMbf"}):
            try:
                cleaned = self.remove_garbage(row.text)

                if is_csv:
                    resp['products'].append(self.format_dict(product, cleaned))
                    resp['meta'].append(float(cleaned[1]))
                else:
                    generate_insert(product, cleaned[0], 'dunnes', cleaned[1], None)

            except AttributeError as e:
                continue
            except IndexError as e:
                continue
        return resp