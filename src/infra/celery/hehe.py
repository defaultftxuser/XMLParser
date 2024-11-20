from src.infra.celery.tasks import (
    start_parse_xml_and_save_products,
)

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
result = start_parse_xml_and_save_products.apply_async(args=[xml_data])

# Получение результата
output = result.get(timeout=10)  # Подождите до 10 секунд для получения результата
print("Parsed products:", output)
