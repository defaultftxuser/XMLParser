import datetime

from lxml import etree
from lxml.etree import XMLSyntaxError

from src.common.converters.converters import convert_into_kopeck
from src.domain.entities.base_lxml import BaseLxmlEntity
from src.domain.entities.lxml_entities import ProductEntity, QuantityEntity, PriceEntity


class LXMLParser:

    def parsing(self, lxml_data: str, element: str = "//product") -> [BaseLxmlEntity]:
        try:
            root = etree.fromstring(lxml_data)
            sale_date = datetime.datetime.strptime(
                (root.attrib.get("date")), "%Y-%m-%d"
            ).date()

            elements = root.xpath(element)
            extracted_data: dict[str, BaseLxmlEntity] = {}

            for element in elements:
                current_element_name = element.findtext("name")
                current_element_quantity = element.findtext("quantity")
                current_element_price = element.findtext("price")
                current_element_category = element.findtext("category")
                if any(
                    element is None
                    for element in (
                        current_element_category,
                        current_element_price,
                        current_element_quantity,
                    )
                ):
                    continue
                if current_element_name in extracted_data:
                    extracted_data[current_element_name].quantity += int(
                        element.findtext("quantity")
                    )
                else:
                    extracted_data[current_element_name] = BaseLxmlEntity(
                        sale_date=sale_date,
                        product=ProductEntity(current_element_name),
                        quantity=QuantityEntity(int(current_element_quantity)),
                        price=PriceEntity(
                            convert_into_kopeck(float(current_element_price))
                        ),
                        category_name=current_element_category,
                    )
            return extracted_data.values()
        except XMLSyntaxError:
            ...
        except etree.XPathEvalError:
            ...
        except ValueError:
            ...
