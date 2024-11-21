import datetime

from lxml import etree
from lxml.etree import XMLSyntaxError

from src.common.converters.converters import convert_into_kopeck
from src.common.settings.logger import get_logger
from src.domain.entities.base_lxml import BaseLxmlEntity
from src.domain.entities.lxml_entities import ProductEntity, QuantityEntity, PriceEntity

logger = get_logger(__name__)


class LXMLParser:

    @staticmethod
    # TODO extract validation
    def parsing(lxml_data: str, element: str = "//product") -> [BaseLxmlEntity]:
        try:
            logger.info("Starting XML parsing.")
            try:
                root = etree.fromstring(lxml_data)
            except etree.XMLSyntaxError as e:
                logger.error(f"XML syntax error: {e}")
                raise ValueError("Invalid XML format.") from e

            logger.debug("XML parsed successfully. Extracting sale date.")

            sale_date_str = root.attrib.get("date")
            if not sale_date_str:
                logger.warning("Missing 'date' attribute in XML root element.")
                raise ValueError("Missing 'date' attribute in XML data.")

            try:
                sale_date = datetime.datetime.strptime(sale_date_str, "%Y-%m-%d").date()
            except ValueError as e:
                logger.error(
                    f"Invalid date format: {sale_date_str}. Expected format YYYY-MM-DD."
                )
                raise ValueError(
                    "Invalid 'date' attribute format. Expected 'YYYY-MM-DD'."
                ) from e

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
                    el is None
                    for el in (
                        current_element_category,
                        current_element_price,
                        current_element_quantity,
                    )
                ):
                    logger.warning(
                        f"Skipping element {current_element_name} due to missing data."
                    )
                    continue

                try:
                    current_element_quantity = int(current_element_quantity)
                except (ValueError, TypeError) as e:
                    logger.warning(
                        f"Invalid quantity value '{current_element_quantity}' for product '{current_element_name}'. Skipping."
                    )
                    continue

                try:
                    current_element_price = float(current_element_price)
                except (ValueError, TypeError) as e:
                    logger.warning(
                        f"Invalid price value '{current_element_price}' for product '{current_element_name}'. Skipping."
                    )
                    continue

                try:
                    price_in_kopeck = convert_into_kopeck(current_element_price)
                except Exception as e:
                    logger.error(
                        f"Error converting price for product {current_element_name}: {e}"
                    )
                    continue

                if current_element_name in extracted_data:
                    extracted_data[
                        current_element_name
                    ].quantity += current_element_quantity
                    logger.debug(
                        f"Updated quantity for {current_element_name}: {extracted_data[current_element_name].quantity}"
                    )
                else:
                    extracted_data[current_element_name] = BaseLxmlEntity(
                        sale_date=sale_date,
                        product=ProductEntity(current_element_name),
                        quantity=QuantityEntity(current_element_quantity),
                        price=PriceEntity(price_in_kopeck),
                        category_name=current_element_category,
                    )
                    logger.debug(
                        f"Added new product to extracted data: {current_element_name}"
                    )

            logger.info(f"Parsed and extracted {len(extracted_data)} products.")
            return extracted_data.values()

        except ValueError as e:
            logger.error(f"Value error during parsing: {e}")
            raise
        except Exception as e:
            logger.error(f"Error during XML parsing: {e}")
            raise
