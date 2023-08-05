from simple_ddl_parser import DDLParser

ddl = """
CREATE TABLE order_items
    ( order_id           NUMBER(12) NOT NULL,
      line_item_id       NUMBER(3)  NOT NULL,
      product_id         NUMBER(6)  NOT NULL,
      unit_price         NUMBER(8,2),
      quantity           NUMBER(8),
      CONSTRAINT order_items_fk
      FOREIGN KEY(order_id) REFERENCES orders(order_id)
    )
    PARTITION BY (order_items_fk);
"""
result = DDLParser(ddl).run(group_by_type=True)
import pprint

pprint.pprint(result)
