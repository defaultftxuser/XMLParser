import datetime

from lxml import etree

from src.common.converters.converters import convert_into_kopeck
from src.common.settings.logger import get_logger
from src.domain.entities.base_lxml import BaseLxmlEntity
from src.domain.entities.lxml_entities import ProductEntity, QuantityEntity, PriceEntity

logger = get_logger(__name__)


class LXMLParser:

    def parsing(self, lxml_data: str, element: str = "//product") -> [BaseLxmlEntity]:
        try:
            logger.info("Starting XML parsing.")
            root = etree.fromstring(lxml_data)
            logger.debug("XML parsed successfully. Extracting sale date.")
            sale_date = datetime.datetime.strptime(
                (root.attrib.get("date")), "%Y-%m-%d"
            ).date()
            logger.debug(f"Sale date extracted: {sale_date}")

            elements = root.xpath(element)
            extracted_data: dict[str, BaseLxmlEntity] = {}

            for element in elements:
                current_element_name = element.findtext("name")
                current_element_quantity = element.findtext("quantity")
                current_element_price = element.findtext("price")
                current_element_category = element.findtext("category")

                logger.debug(f"Processing element: {current_element_name}")

                if any(
                    element is None
                    for element in (
                        current_element_category,
                        current_element_price,
                        current_element_quantity,
                    )
                ):
                    logger.warning(
                        f"Skipping element {current_element_name} due to missing data."
                    )
                    continue

                if current_element_name in extracted_data:
                    extracted_data[current_element_name].quantity += int(
                        element.findtext("quantity")
                    )
                    logger.debug(
                        f"Updated quantity for {current_element_name}: {extracted_data[current_element_name].quantity}"
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
                    logger.debug(
                        f"Added new product to extracted data: {current_element_name}"
                    )

            logger.info(f"Parsed and extracted {len(extracted_data)} products.")
            return extracted_data.values()

        except Exception as e:
            logger.error(f"Error during XML parsing: {e}")
            raise
