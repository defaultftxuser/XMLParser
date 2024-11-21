from src.infra.celery.tasks import (
    start_parse_xml_and_save_products,
)
from src.logic.xml_parser import LXMLParser

xml_data = """
<sales_data date="2024-01-01">
    <products>
        <product>
            <id>1</id>
            <name>Product A</name>
            <quantity>100</quantity>
            <price>1500.00</price>
            <category>Electronics</category>
        </product>
        <product>
            <id>2</id>
            <name>Product B</name>
            <quantity>100</quantity>
            <price>1500.00</price>
            <category>Electronics</category>
        </product>
        <!-- More products... -->
    </products>
</sales_data>
"""


# Запуск задачи через Celery
result = LXMLParser().parsing(xml_data)
print(result)
