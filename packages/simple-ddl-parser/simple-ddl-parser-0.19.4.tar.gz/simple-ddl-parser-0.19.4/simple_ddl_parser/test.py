from simple_ddl_parser import DDLParser

ddl = """
CREATE TABLE table_name ( table_id INT64, a_column STRING, another_column BOOLEAN, a_partion_column DATE ) PARTITION BY a_partion_column;
"""
result = DDLParser(ddl).run(group_by_type=True)
import pprint

pprint.pprint(result)
